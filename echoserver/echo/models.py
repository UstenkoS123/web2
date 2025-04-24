# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Books(models.Model):
    book_name = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'books'

class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    login = models.CharField(max_length=100, unique=True, db_column='login', primary_key=True)
    password = models.CharField(max_length=100, db_column='password')
    email = models.EmailField(max_length=100 , db_column='email')
    name = models.CharField(max_length=100, db_column='name')

    # Роли
    ROLES = (
        ('guest', 'Гость'),
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=45, choices=ROLES, default='guest', db_column='role')

    # Отключаем все стандартные поля Django
    last_login = None
    is_superuser = None
    is_staff = None
    is_active = True # пользователь активен (необходимо для входа)

    objects = UserManager()

    USERNAME_FIELD = 'login'  # Поле для входа (логин)
    REQUIRED_FIELDS = ['email', 'name']  # Обязательные поля

    class Meta:
        db_table = 'users'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()
    
    class Meta:
        db_table = 'orders'

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book_id = models.IntegerField()
    quantity = models.IntegerField()
    
    class Meta:
        db_table = 'orders_items'