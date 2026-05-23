import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindly_project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
password = 'admin123'  # muda para uma password à tua escolha
email = 'admin@admin.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print(f'Superuser "{username}" criado com sucesso!')
else:
    print(f'Utilizador "{username}" já existe.')