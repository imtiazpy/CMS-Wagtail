from django import template
from django.utils.translation import get_language
from wagtail.models import Locale
from ..models import StickyContactLink

register = template.Library()


# @register.simple_tag()
# def get_contact_link():
#     current_language = get_language()
#     current_locale = Locale.objects.get(language_code=current_language)
#     try:
#         contact_page = ContactPage.objects.get(locale=current_locale)
#         return contact_page.url
#     except ContactPage.DoesNotExist:
#         return '#'
    

@register.simple_tag()
def get_sticky_contact():
    try:
        current_language = get_language()
        sticky_obj = StickyContactLink.objects.get(language=current_language)
        return sticky_obj.page.url
    except StickyContactLink.DoesNotExist:
        return "#"
