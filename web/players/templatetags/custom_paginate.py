from django import template

register = template.Library()

# simple custom template tag to update page param
# while maintaining current url
@register.simple_tag(takes_context=True)
def custom_paginate(context, **kwargs):
    params = context['request'].GET.copy()
    params['page'] = kwargs['page']
    #params['page'] = page
    return params.urlencode()