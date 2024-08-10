from django import template
from store.models import Category
from store.utils import Userscart

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_card_items(request):
    cart = Userscart(request)
    return cart.get_cart_info()
