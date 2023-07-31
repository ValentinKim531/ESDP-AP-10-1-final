from django import template

register = template.Library()


@register.filter(name='endswith')
def endswith(value, arg):
    return str(value).endswith(str(arg))


@register.filter(name='startswith')
def endswith(value, arg):
    return str(value).startswith(str(arg))
