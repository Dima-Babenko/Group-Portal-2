from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Витягування значення за ключем зі словника."""
    return dictionary.get(key)