from django import template
from django.utils.translation import get_language

from site_settings.models import CookieConsentSettings

register = template.Library()

@register.simple_tag()
def get_cookie():
    try:
        language = get_language()
        return CookieConsentSettings.objects.get(language=language)
    except CookieConsentSettings.DoesNotExist:
        return None