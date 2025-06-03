from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def stripe_publishable_key() -> str:
    return settings.STRIPE_PUBLISHABLE_KEY
