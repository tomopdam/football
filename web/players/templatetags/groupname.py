from django import template

register = template.Library()

# convert integer into euros
# if we need greater functionality we should use a library
@register.filter
def groupname(value):
    groups = {
        'GK' : 'Goalkeeper',
        'FB' : 'Fullback',
        'HB' : 'Halfback',
        'FP' : 'Forward playing'
    }
    if value not in groups.keys():
        return ""
    return groups[value]