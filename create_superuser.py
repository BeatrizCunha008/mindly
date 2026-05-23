import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindly_project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'BeatrizCunha'

try:
    u = User.objects.get(username=username)
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print(f'Utilizador "{username}" promovido a superuser!')
except User.DoesNotExist:
    print(f'Utilizador "{username}" não encontrado.')