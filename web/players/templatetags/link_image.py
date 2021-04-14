from django import template

register = template.Library()

# note-- this is deprecated
# since i checked the photos in bulk and updated
# the DB

# generate url to external image based on player.id_ext
@register.simple_tag
def link_image(id_ext):
    # pad to 6 digits if needed
    full = str(id_ext).zfill(6)
    part1 = full[:3]
    part2 = full[3:]
    return 'https://cdn.sofifa.com/players/'+part1+'/'+part2+'/21_120.png'