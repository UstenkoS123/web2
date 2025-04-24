from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.functional import SimpleLazyObject
from echo.models import * # Импорт нашей модели
from .forms import * # Импортируем заполняемые формы
from .decorators import admin_required, user_required


def bookList(request):
    books = Books.objects.all()  # Получаем все записи из таблицы books
    paginator = Paginator(books, 5) # 5 книг на страницу
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-запроса
    books = paginator.get_page(page_number)  # Получаем книги для текущей страницы

    return render(request, 'echo/book_list.html', {'books': books})

# Просмотр корзины
def cart_list(request):
    cart = request.session.get('cart', {}) # корзина из сессии
    book_ids = [int(book_id) for book_id in cart.keys()] # книги из сессии
    books_in_cart = Books.objects.filter(id__in=book_ids) # получаем книги из базы данных
    
    # Добавляем количество из корзины к каждой книге
    for book in books_in_cart:
        book.quantity = cart[str(book.id)]['quantity']
        book.total_price = book.price * book.quantity
    
    # Применяем пагинацию
    paginator = Paginator(books_in_cart, 10)  # 10 книг на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Считаем общую сумму
    total = sum(book.total_price for book in books_in_cart)
    
    return render(request, 'echo/cart_list.html', {
        'page_obj': page_obj,
        'total': total
    })

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

# Отображение данных личного кабинета
@user_required
def cabinetView(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'echo/cabinet.html', context)

# Представление для изменения имени пользователя
@user_required
def cabinetChangeName(request):
    if request.method == 'POST':
        form = ChangeNameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('cabinet')
    else:
        form = ChangeNameForm(instance=request.user)
    
    return render(request, 'echo/cabinet_edit_name.html', {'form': form})

# Представление для изменения почты пользователя
@user_required
def cabinetChangeEmail(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('cabinet')
    else:
        form = ChangeEmailForm(instance=request.user)
    
    return render(request, 'echo/cabinet_edit_email.html', {'form': form})

# Представление для изменения пароля пользователя
@user_required
def cabinetChangePassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ChangePasswordForm(instance=request.user)
    
    return render(request, 'echo/cabinet_edit_password.html', {'form': form})

# Добавление в корзину
@user_required
def addToCart(request, id):
    book = get_object_or_404(Books, id=id)

    # Инициализируем корзину в сессии, если её нет
    if 'cart' not in request.session:
        request.session['cart'] = {}
    cart = request.session.get('cart', {})

    # добавление книги в корзину / увеличение количества книг
    if str(id) in cart:
        cart[str(id)]['quantity'] += 1
    else:
        cart[str(id)] = {
            'book_id': book.id,
            'book_name': book.book_name,  # Автоматически подтягиваем данные
            'author': book.author,
            'price': float(book.price),  # Decimal -> float для сериализации
            'quantity': cart.get(str(id), {}).get('quantity', 0) + 1
        }

    request.session['cart'] = cart
    return redirect('book_list')

# Очистка корзины
def cart_clear(request):
    cart = request.session['cart']
    if cart:
        request.session['cart'] = {}
    return redirect('cart_list')

# Оформление заказа
def create_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Ваша корзина пуста")
        return redirect('cart_list')

    try:
        # Создаём заказ
        total = int(sum(item['price'] * item['quantity'] for item in cart.values()))
        order = Order.objects.create(
            user=request.user,
            total_price=total
        )
        
        # Создаём элементы заказа
        for book_id, item in cart.items():
            OrderItems.objects.create(
                order=order,
                book_id=item['book_id'],
                quantity=item['quantity']
            )
        
        # Очищаем корзину
        request.session['cart'] = {}
        return redirect('orders_list')
    
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return redirect('cart_list')
    
# Страница со всеми заказами
def orders_list(request):
    orders_obj = Order.objects.filter(user__login=request.user.login)
    
    # Применяем пагинацию
    paginator = Paginator(orders_obj, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    return render(request, 'echo/orders_list.html', {'orders': orders})

# Информация по заказу
def order_info(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    order_items = OrderItems.objects.filter(order=order)

    # Получаем информацию о книгах
    book_ids = [item.book_id for item in order_items]
    books_info = Books.objects.filter(id__in=book_ids)

    # Добавляем количество книг в инфу
    quantity_map = {item.book_id: item.quantity for item in order_items}
    for book in books_info:
        book.quantity = quantity_map[book.id]
    
    # Применяем пагинацию
    paginator = Paginator(books_info, 10)  # 10 книг на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Собираем данные для шаблона
    context = {
        'order': order,
        'books_info': books_info,
        'page_obj': page_obj
    }

    return render(request, 'echo/order_info.html', context)

def homePageView(request):
    return HttpResponse("Hello world!")
