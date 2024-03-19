from django import template
from django.core.exceptions import FieldDoesNotExist

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, '---')


@register.filter(name='verbose_attr')
def verbose_attribute(object, attribute_name):
    try:
        return object._meta.get_field(attribute_name).verbose_name.capitalize()
    except FieldDoesNotExist:
        return attribute_name.replace('_', ' ').capitalize()
