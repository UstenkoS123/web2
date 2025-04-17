from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Books, User

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['book_name', 'author', 'price']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин', 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'  # Переопределяем label

class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, label='Имя пользователя')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('login', 'email', 'name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Переименовываем поле 'login' для красивого отображения
        self.fields['login'].label = 'Логин'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

    # Задаем роль пользователя
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'user'
        user.save()
        return user