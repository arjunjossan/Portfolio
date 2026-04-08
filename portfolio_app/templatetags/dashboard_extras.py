import json
from pathlib import Path

from django import template


register = template.Library()


@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name, "")


@register.filter
def format_dashboard_value(value):
    if value is None or value == "":
        return "—"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (list, tuple)):
        if not value:
            return "—"
        if len(value) == 1:
            return str(value[0])
        preview = ", ".join(str(item) for item in value[:3])
        return f"{preview} (+{len(value) - 3})" if len(value) > 3 else preview
    if isinstance(value, dict):
        if not value:
            return "—"
        preview_items = list(value.items())[:2]
        preview = ", ".join(f"{key}: {item}" for key, item in preview_items)
        return f"{preview}..." if len(value) > 2 else preview
    if hasattr(value, "url") and hasattr(value, "name"):
        return Path(value.name).name
    if hasattr(value, "strftime"):
        try:
            return value.strftime("%b %d, %Y")
        except Exception:
            return str(value)
    if hasattr(value, "all"):
        related_values = list(value.all()[:3])
        return ", ".join(str(item) for item in related_values) if related_values else "—"
    try:
        if len(str(value)) > 90 and not isinstance(value, (int, float)):
            return f"{str(value)[:87]}..."
    except Exception:
        pass
    return str(value)
