from .models import Product, CartProduct, Cart


class Userscart:
    def __init__(self, request, product_id=None, quantity=None, action=None):
        self.user = request.user
        if product_id and action and quantity:
            self.add_or_delete(product_id, quantity, action)
    def get_cart_info(self):
        cart, created = Cart.objects.get_or_create(
            user=self.user
        )
        cart_products = cart.cartproduct_set.all()
        cart_total_quantity = cart.get_cart_total_quantity
        cart_total_price = cart.get_cart_total_price
        get_cart_quantity = cart.get_cart_quantity

        return {
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'cart_products': cart_products,
            'get_cart_quantity': get_cart_quantity,
            'cart': cart,
        }

    def add_or_delete(self, product_id, quantity, action):
        cart = self.get_cart_info()['cart']
        product = Product.objects.get(pk=product_id)
        cart_product, created = CartProduct.objects.get_or_create(product=product,
                                                                  cart=cart)
        if action == 'add':
            cart_product.quantity += quantity
        else:
            cart_product.quantity -= quantity
        cart_product.save()

        if cart_product.quantity <= 0:
            cart_product.delete()

    def clear(self):
        cart = self.get_cart_info()['cart']
        cart_products = cart.cartproduct_set.all()
        for product in cart_products:
            product.delete()
        cart.save()