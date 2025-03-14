from django import template

register = template.Library()

@register.filter
def to_thai_year(value):
    return value + 543
