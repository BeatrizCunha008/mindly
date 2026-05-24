from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Perfil, RelacaoPsicologoPaciente, RegistoHumor, EntradaDiario, FotoAlbum

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [PerfilInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(RelacaoPsicologoPaciente)
admin.site.register(RegistoHumor)
admin.site.register(EntradaDiario)
admin.site.register(FotoAlbum)