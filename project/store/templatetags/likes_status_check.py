from django import template
from store.models import Liked

register = template.Library()


@register.simple_tag()
def check_status(user, product_id):
    return Liked.objects.filter(user=user, product_id=product_id).exists()

