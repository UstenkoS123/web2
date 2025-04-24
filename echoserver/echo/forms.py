from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
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
    
# Форма изменения имени
class ChangeNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите новое имя'
            })
        }
        labels = {
            'name': 'Новое имя'
        }

    current_password = forms.CharField(
        label='Ваш пароль:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль'
        }),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        user = self.instance

        if not user.check_password(current_password):
            raise forms.ValidationError("Неверный пароль. Попробуйте снова.")
        
        return cleaned_data

# Форма изменения почты
class ChangeEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите новую почту'
            })
        }
        labels = {
            'email': 'Новая почта'
        }

    current_password = forms.CharField(
        label='Ваш пароль:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль'
        }),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        user = self.instance

        if not user.check_password(current_password):
            raise forms.ValidationError("Неверный пароль. Попробуйте снова.")
        
        return cleaned_data
    
# Форма изменения пароля
class ChangePasswordForm(forms.ModelForm):
    current_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите текущий пароль'
        }),
        required=True
    )
    
    new_password = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый пароль'
        }),
        required=True
    )
    
    confirm_password = forms.CharField(
        label='Подтвердите новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите новый пароль'
        }),
        required=True
    )

    class Meta:
        model = User
        fields = []  # Не нужны поля модели, только пароли

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        user = self.instance

        # Проверка текущего пароля
        if not user.check_password(current_password):
            raise ValidationError("Текущий пароль указан неверно")
        
        # Проверка совпадения новых паролей
        if new_password and new_password != confirm_password:
            raise ValidationError("Новые пароли не совпадают")
        
        # Валидация сложности пароля
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            raise ValidationError(e.messages)
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()
        return user