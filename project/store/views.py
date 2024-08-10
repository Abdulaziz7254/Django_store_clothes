from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from project.settings import STRIPE_SECRET_KEY
from django.urls import reverse
from .utils import Userscart
from .forms import LoginForm, RegistrationForm, AddressForm
from .models import *
import random
import stripe
categories = Category.objects.all()

def index_view(request):
    main_product = random.choice(Product.objects.all())
    products = Product.objects.all()
    context ={

        'products': products,
        'main_product': main_product,


    }
    return render(request, 'store/index.html', context)

def category_view(request, pk):
    category = Category.objects.get(pk=pk)
    products = Product.objects.filter(category=category)
    main_product = random.choice(Product.objects.all())
    context = {
        'products': products,
        'categories': categories,
        'main_product': main_product,
    }
    return render(request, 'store/index.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('index')
            else:
                return redirect('auth')
        else:
            return redirect('auth')



def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            return redirect('auth')
        else:
            return redirect('auth')


def user_logout(request):
    logout(request)
    return redirect('index')

def auth_forms(request):
    context = {
        'login_form': LoginForm(),
        'register_form': RegistrationForm()
    }
    return render(request, 'store/login_regist.html', context)

def liked_add_view(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=pk)
        user = request.user
        liked = Liked.objects.filter(user=user, product=product).exists()
        if liked:
            liked = Liked.objects.get(user=user, product=product)
            liked.delete()
            return redirect('index')
        else:
            liked = Liked.objects.create(user=user, product=product)
            liked.save()
            return redirect('liked')
        return redirect('index')


def list_favorite(request):
    liked = Liked.objects.filter(user=request.user)
    context = {
        'likes': liked,
    }
    return render(request, 'store/liked.html', context)


def add_cart_product(request):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_pk')
        Userscart(request, product_id, quantity, 'add')
        return redirect('cart')



def cart_view(request):
    cart = Userscart(request)
    context = cart.get_cart_info()
    return render(request, 'store/cart.html', context)


def add_or_delete_cart_product(request, pk, action):
    Userscart(request, pk, 1, action)
    return redirect('cart')


def delete_cart_product(request, pk):
    cart_product = CartProduct.objects.get(pk=pk)
    cart_product.delete()
    return redirect('cart')


def clear_cart(request):
    cart = Userscart(request)
    cart.clear()
    return redirect('cart')


def detail_view(request, pk):

    product = Product.objects.get(pk=pk)
    context ={
        'product': product,
    }
    return render(request, 'store/detail.html', context)


def checkout_view(request):
    form = AddressForm()
    context = Userscart(request).get_cart_info()
    context['form'] = form
    return render(request,'store/checkout.html',context)
def process_function(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
        cart = Userscart(request)
        cart_info = cart.get_cart_info()
        cart_products = cart_info['cart_products']
        order = Order.objects.create(user=request.user, address=address)
        for cart_product in cart_products:
            order_item = OrderItem.objects.create(order=order,
                                                  product=cart_product.product,
                                                  quantity=cart_product.quantity,
                                                  unit_price=cart_product.product.price)
            order_item.save()
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': cart_product.product.name
                    },
                    'unit_amount': int(cart_product.product.price * 100)
                },
            'quantity': cart_product.quantity
            } for cart_product in cart_info['cart_products']]
        stripe.api_key = STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('checkout'))
        )
        return redirect(session.url, 303)


def success_payment(request):
    cart = Userscart(request)
    order = Order.objects.latest('placed_at')
    order.status = 'C'
    order.save()
    cart.clear()
    return redirect('index')