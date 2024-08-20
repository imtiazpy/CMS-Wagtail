from django import template
import random

register = template.Library()

@register.filter()
def shuffle(value):
    random.shuffle(value)
    return value