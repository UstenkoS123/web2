from django.core.management.base import BaseCommand
from echo.models import User

# Создаём админа
class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(login='admin').exists():
            User.objects.create(
                login='admin',
                email='ustenkos@list.ru',
                name='Admin',
                role='admin'
            )
            user = User.objects.get(login='admin')
            user.set_password('Karam8576op')  # Установите надежный пароль
            user.save()
        else:
            self.stdout.write(self.style.WARNING('Админ уже существует'))