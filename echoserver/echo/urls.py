from django.urls import path
from .views import bookList, bookDelete, bookEdit, bookAdd

urlpatterns = [
    path('', bookList, name='home'),
    path('books/', bookList, name='book_list'),
    path('books/delete/<int:id>/', bookDelete, name='bookDelete'),
    path('books/edit/<int:id>/', bookEdit, name='bookEdit'),
    path('books/add/', bookAdd, name="bookAdd")
]