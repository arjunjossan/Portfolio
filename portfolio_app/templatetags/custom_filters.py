from django import template

register = template.Library()


@register.filter
def dict_items(value):
    if isinstance(value, dict):
        return value.items()
    return []


@register.filter
def stars(value):
    try:
        rating = int(value)
    except (TypeError, ValueError):
        rating = 0
    return range(max(rating, 0))
