from django import urls
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
from urllib.parse import urlparse
from wagtail.models import Page, Locale


def set_language_from_url(request, language_code):
    # call url with ?next=<<translated url>> to redirect to translated page
    # if no next url supplied, will attempt to find it from referring url
    # if fails that, will send to home page of the language_code
    # if requested language is not a registered locale, send to home page
    try:
        requested_locale = Locale.objects.get(language_code=language_code)
    except Locale.DoesNotExist:
        return HttpResponseRedirect("/")

    # if /?next= missing from referring url, attempt to translate
    next_url = request.GET.get("next")
    if not next_url:
        next_url = find_next_url(request, requested_locale)

    # activate the language, set the cookie (gets around expiring session cookie issue), redirect to translated page
    translation.activate(language_code)
    response = HttpResponseRedirect(next_url)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, language_code, max_age=60 * 60 * 24 * 365
    )

    return response


def find_next_url(request, requested_locale):
    # /?next= missing from referring url, attempt to translate
    try:
        # get the full path of the referring page;
        previous = request.META["HTTP_REFERER"]

        try:
            # split off the path of the previous page
            prev_path = urlparse(previous).path
            # Your locale home pages must have the language code as the slug for the following line to work
            # url_path uses the locale home page slug instead of the language code used in the resolved url
            prev_page = Page.objects.get(url_path=prev_path).specific

            # Find translation of referring page
            # Default to home page if nothing matches
            next_page = prev_page.translations.get(
                requested_locale.language_code)
            next_url = next_page or find_closest_translation(
                prev_page, requested_locale
            )

        except Page.DoesNotExist:
            # previous page is not a Wagtail Page, try if previous path can be translated by
            # changing the language code
            next_url = urls.translate_url(
                previous, requested_locale.language_code)

            # if no translation is found, translate_url will return the original url
            # in that case, go to the home page in the requested language
            if next_url == previous:
                next_url = "/"

    except KeyError:
        # if for some reason the previous page cannot be found, go to the home page
        next_url = "/"

    return next_url


def find_closest_translation(page, locale):
    parent = page.get_parent().specific
    next_page = parent.translations.get(locale.language_code)
    return next_page or (
        find_closest_translation(parent, locale) if parent.depth >= 3 else "/"
    )
