from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from echo.models import Books # Импорт нашей модели
from .forms import BookForm, LoginForm, RegisterForm # Импортируем заполняемые формы
from .decorators import admin_required, user_required


def bookList(request):
    books = Books.objects.all()  # Получаем все записи из таблицы books
    paginator = Paginator(books, 5) # 5 книг на страницу
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-запроса
    books = paginator.get_page(page_number)  # Получаем книги для текущей страницы

    return render(request, 'echo/book_list.html', {'books': books})

@admin_required
def bookDelete(request, id):
    book = get_object_or_404(Books, id=id)  # Находим книгу по ID
    book.delete()  # Удаляем книгу
    return redirect('book_list')  # Перенаправляем на страницу со списком книг

@admin_required
def bookEdit(request, id):
    book = get_object_or_404(Books, id=id)  # Находим книгу по ID

    # Если данные отправлены, обрабатываем форму
    if request.method == 'POST':
        print("POST data:", request.POST)  # Выводим данные POST-запроса
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('book_list')  # Перенаправляем на список книг
        else:
            # Выводим ошибки формы в консоль
            print("Form errors:", form.errors)
    # Если это GET-запрос, отображаем форму с текущими данными
    else:
        form = BookForm(instance=book)

    return render(request, 'echo/edit_book.html', {'form': form})

@user_required
def bookAdd(request):
    # Если данные отправлены, обрабатываем форму
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем новую книгу
            return redirect('book_list')  # Перенаправляем на список книг
    # Если это GET-запрос, отображаем пустую форму
    else:
        form = BookForm()

    return render(request, 'echo/add_book.html', {'form': form})

# Представление авторизации
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login_field = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=login_field, password=password)

            if user is not None:
                login(request, user)
                return redirect('book_list')
    else:
        form = LoginForm()
    return render(request, 'echo/login.html', {'form': form})

# Представление регистрации
def registerView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.login = form.cleaned_data['login']  # Явное сохранение логина
            user.save()
            login(request, user)
            return redirect('home')  # Редирект после успешной регистрации (на страницу авторизации)
    else:
        form = RegisterForm()
    return render(request, "echo/register.html", {"form": form})

# Представление выхода из аккаунта
def logoutView(request):
    logout(request)
    return redirect("home")

def homePageView(request):
    return HttpResponse("Hello world!")
