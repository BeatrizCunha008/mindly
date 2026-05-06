from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import RegistoHumor, EntradaDiario, FotoAlbum, Perfil


# ── REGISTO DE NOVO UTILIZADOR ──
class RegistoForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ── REGISTO DE HUMOR ──
class RegistoHumorForm(forms.ModelForm):
    class Meta:
        model = RegistoHumor
        fields = ['humor', 'nota']
        widgets = {
            'humor': forms.RadioSelect(),
            'nota': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Como te estás a sentir? (opcional)'
            }),
        }
        labels = {
            'humor': 'Como está o teu humor hoje?',
            'nota': 'Nota',
        }


# ── DIÁRIO DIGITAL ──
class EntradaDiarioForm(forms.ModelForm):
    class Meta:
        model = EntradaDiario
        fields = ['titulo', 'texto']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título da entrada...'}),
            'texto':  forms.Textarea(attrs={'rows': 5, 'placeholder': 'Escreve aqui o teu pensamento...'}),
        }


# ── ÁLBUM DE FOTOS ──
class FotoAlbumForm(forms.ModelForm):
    class Meta:
        model = FotoAlbum
        fields = ['imagem', 'legenda']
        widgets = {
            'legenda': forms.TextInput(attrs={'placeholder': 'Legenda (opcional)...'}),
        }


# ── PERFIL ──
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil', 'tipo', 'telefone', 'data_nasc']
        widgets = {
            'data_nasc': forms.DateInput(attrs={'type': 'date'}),
            'telefone':  forms.TextInput(attrs={'placeholder': '+351 912 345 678'}),
        }


# ── DADOS DO UTILIZADOR (nome/email) ──
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Apelido'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'Email'}),
        }