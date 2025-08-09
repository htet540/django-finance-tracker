from django import template
from django.utils.http import urlencode

register = template.Library()

@register.filter
def money(value, decimals=0):
    """Format decimal with thousands separators."""
    if value is None:
        return "0"
    try:
        f = float(value)
    except Exception:
        return str(value)
    return f"{f:,.{int(decimals)}f}"

@register.simple_tag(takes_context=True)
def qs_set(context, **new_params):
    """
    Build a querystring based on current GET + overrides.
    Usage: href="?{% qs_set page=1 order_by='-date' %}"
    """
    request = context["request"]
    params = request.GET.copy()
    for k, v in new_params.items():
        if v is None:
            params.pop(k, None)
        else:
            params[k] = v
    return urlencode(params, doseq=True)