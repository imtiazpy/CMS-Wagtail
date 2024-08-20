from django import template
from django.utils.translation import get_language
from wagtail.models import Locale
from ..models import NewsIndex

register = template.Library()


@register.simple_tag()
def get_news_link():
    current_language = get_language()
    current_locale = Locale.objects.get(language_code=current_language)
    try:
        news_page = NewsIndex.objects.get(locale=current_locale)
        return news_page.url
    except NewsIndex.DoesNotExist:
        return '#'
