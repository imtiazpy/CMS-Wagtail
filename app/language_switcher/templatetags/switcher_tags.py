from django import template
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.models import Locale

register = template.Library()


@register.simple_tag(takes_context=True)
def language_switcher(context):
    # Build the language switcher
    # determine next_url for each locale if page has translation
    # /lang/<lang-code> redirects to menu.views.set_language_from_url:
    #     path('lang/<str:language_code>/', set_language_from_url),
    # if no ?next= param passed to the view, it will attempt to determine best url from HTTP_REFERER
    # this will happen if non-Wagtail page is served, or if Wagtail page has no translation

    current_lang = Locale.get_active()
    switcher = {'alternatives': []}

    page = context.get('page', False)
    if page:
        for locale in Locale.objects.all():
            if locale == current_lang:
                switcher['current'] = locale
            else:  # add the link to switch language
                next_url = next(
                    (item for item in page.alternates if item['lang_code'] == locale.language_code), None)
                if next_url:
                    next_url = next_url['location']
                    if isinstance(page, RoutablePageMixin):
                        next_url += context['request'].path.replace(
                            page.url, '')
                    next_url = f'?next={next_url}'

                switcher['alternatives'].append(
                    {
                        'name': locale.get_display_name(),
                        'code': locale.language_code,
                        'url': f'/lang/{locale.language_code}/{next_url}'
                    }
                )
    else:
        for locale in Locale.objects.all():
            if locale == current_lang:
                switcher['current'] = locale
            else:
                switcher['alternatives'].append(
                    {
                        'name': locale.get_display_name(),
                        'code': locale.language_code,
                        'url': f'/lang/{locale.language_code}/'
                    }
                )
    return switcher
