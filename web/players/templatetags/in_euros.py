from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

# convert integer into euros
# if we need greater functionality we should use a library
@register.simple_tag
def in_euros(value):
    if not value:
        return "€ 0"
    return "€ " + intcomma(value)