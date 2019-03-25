from django import template

register = template.Library()

@register.filter()
def minus(val):
    return 5-val

@register.filter()
def getrange(val):
    return range(val)
