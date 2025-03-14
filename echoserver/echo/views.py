from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from echo.models import Books # Импорт нашей модели
from .forms import BookForm # Импортируем книжную форму

def bookList(request):
    books = Books.objects.all()  # Получаем все записи из таблицы books
    paginator = Paginator(books, 5) # 5 книг на страницу
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-запроса
    books = paginator.get_page(page_number)  # Получаем книги для текущей страницы

    return render(request, 'echo/book_list.html', {'books': books})

def bookDelete(request, id):
    book = get_object_or_404(Books, id=id)  # Находим книгу по ID
    book.delete()  # Удаляем книгу
    return redirect('home')  # Перенаправляем на страницу со списком книг

def bookEdit(request, id):
    book = get_object_or_404(Books, id=id)  # Находим книгу по ID

    # Если данные отправлены, обрабатываем форму
    if request.method == 'POST':
        print("POST data:", request.POST)  # Выводим данные POST-запроса
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('home')  # Перенаправляем на список книг
        else:
            # Выводим ошибки формы в консоль
            print("Form errors:", form.errors)
    # Если это GET-запрос, отображаем форму с текущими данными
    else:
        form = BookForm(instance=book)

    return render(request, 'echo/edit_book.html', {'form': form})

def bookAdd(request):
    # Если данные отправлены, обрабатываем форму
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем новую книгу
            return redirect('home')  # Перенаправляем на список книг
    # Если это GET-запрос, отображаем пустую форму
    else:
        form = BookForm()

    return render(request, 'echo/add_book.html', {'form': form})

def homePageView(request):
    return HttpResponse("Hello world!")
