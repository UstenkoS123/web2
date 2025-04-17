from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

# Декоратор, требующий роль для использования функции
def role_required(*roles):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            # для неавторизованных пользователей
            if not request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            # ну а вдруг роли нет в ролях
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

# Декораторы для проверки на админа и пользователя
admin_required = role_required('admin')
user_required = role_required('user', 'admin')