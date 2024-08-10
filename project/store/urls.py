from django.urls import path
from .views import *

urlpatterns = [
    path('',index_view, name='index'),
    path('category/<int:pk>',category_view, name='category'),
    path('shop/<int:pk>',category_view, name='shop'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('auth/', auth_forms, name='auth'),
    path('liked_add/<int:pk>/', liked_add_view, name='add_to_liked'),
    path('liked/', list_favorite, name='liked'),
    path('card/', cart_view, name='cart'),
    path('add_product/', add_cart_product, name='add'),
    path('change_quantity/<int:pk>/<str:action>', add_or_delete_cart_product, name='quantity'),
    path('delete_cart_product/<int:pk>/', delete_cart_product, name='delete_cart_product'),
    path('clear_cart/', clear_cart, name='clear'),
    path('detail/<int:pk>/', detail_view, name='detail'),
    path('checkout/',checkout_view, name='checkout'),
    path('process_function/',process_function, name='process_function'),
    path('success/', success_payment, name='success')

]