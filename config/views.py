from django.template.defaulttags import register

@register.filter
def get_natural_range(value):
    return range(1, value + 1)