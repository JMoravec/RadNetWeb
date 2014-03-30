__author__ = 'Joshua Moravec'
from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''


@register.filter
def field_type(obj):
    return obj.__class__.__name__