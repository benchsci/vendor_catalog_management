from django import template

register = template.Library()


@register.inclusion_tag('google_auth_button.html')
def google_auth_button(title):
    return {'title': title}
