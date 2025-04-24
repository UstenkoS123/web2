from django.urls import path
from .views import *

urlpatterns = [
    path('', loginView, name='home'),
    path('logout/', logoutView, name='logout'),
    path('register/', registerView, name='register'),
    path('books/', bookList, name='book_list'),
    path('books/delete/<int:id>/', bookDelete, name='bookDelete'),
    path('books/edit/<int:id>/', bookEdit, name='bookEdit'),
    path('books/add/', bookAdd, name="bookAdd"),
    path('cabinet/', cabinetView, name="cabinet"),
    path('cabinet/edit_name', cabinetChangeName, name="cabinet_edit_name"),
    path('cabinet/edit_email', cabinetChangeEmail, name="cabinet_edit_email"),
    path('cabinet/edit_password', cabinetChangePassword, name="cabinet_edit_password"),
    path('cart/', cart_list, name="cart_list"),
    path('cart_clear/', cart_clear, name="cart_clear"),
    path('addtocart/<int:id>', addToCart, name="add_to_cart"),
    path('create_order/', create_order, name="create_order"),
    path('orders_list', orders_list, name='orders_list'),
    path('order_info/<int:id>/', order_info, name='order_info')
]