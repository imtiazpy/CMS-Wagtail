from django import template
from django.utils.translation import get_language


from ..models import Menu, QuickMenu

register = template.Library()

@register.simple_tag()
def get_menu(menu_type):
    try:
        language = get_language()
        menu = Menu.objects.get(menu_type=menu_type, language=language)
        return menu.menu_items.all().order_by('position')
    except Menu.DoesNotExist:
        return None
    

@register.simple_tag()
def get_quick_menu():
    try:
        language = get_language()
        quick_menu = QuickMenu.objects.get(language=language)
        return quick_menu.quick_menu_items.all().order_by('position')
    except QuickMenu.DoesNotExist:
        return None