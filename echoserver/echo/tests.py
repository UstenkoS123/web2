from django.test import TestCase
from django.core.paginator import Paginator
from .models import Books

# Create your tests here.

class BookModelTests(TestCase):

    def setUp(self):
        # Создание тестовых данных
        self.book1 = Books.objects.create(book_name="Книга 1", author="Автор 1", price=100.00)
        self.book2 = Books.objects.create(book_name="Книга 2", author="Автор 2", price=200.00)

    def test_add_book(self):
        """Проверка добавления книги"""
        book_count = Books.objects.count()
        Books.objects.create(book_name="Книга 3", author="Автор 3", price=150.00)
        self.assertEqual(Books.objects.count(), book_count + 1)

    def test_change_book(self):
        """Проверка изменения существующей книги"""
        self.book1.title = "Измененная Книга 1"
        self.book1.save()
        updated_book = Books.objects.get(id=self.book1.id)
        self.assertEqual(updated_book.book_name, "Измененная Книга 1")

    def test_delete_book(self):
        """Проверка удаления книги"""
        book_count = Books.objects.count()
        self.book2.delete()
        self.assertEqual(Books.objects.count(), book_count - 1)

    def test_pagination(self):
        """Проверка пагинации"""
        # Создание дополнительных книг для теста пагинации
        for i in range(6, 11):
            Books.objects.create(book_name=f"Книга {i}", author=f"Автор {i}", price=i * 100.00)

        # Получение списка книг с пагинацией
        books = Books.objects.all()
        paginator = Paginator(books, 5)  # 5 книг на страницу
        self.assertEqual(paginator.num_pages, 2)  # Должно быть 2 страницы
        self.assertEqual(len(paginator.page(1)), 5)  # Первая страница должна содержать 5 книг
        self.assertEqual(len(paginator.page(2)), 5)  # Вторая страница должна содержать 5 книг
