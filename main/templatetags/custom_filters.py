from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, None)

@register.filter(name='verbose_attr')
def verbose_attribute(object, attibute_name):
    return object._meta.get_field(attibute_name).verbose_name
