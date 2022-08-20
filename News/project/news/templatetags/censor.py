from django import template


register = template.Library()


@register.filter()
def censor(value):
    bad_words = ['редиска', 'злюка']
    for i in bad_words:
        if i in value:
            value = value.replace(i, i[0] + '*'*(len(i) - 1))
            return value
    return value
