from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistoForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EntradaDiarioForm(forms.ModelForm):
    class Meta:
        model  = EntradaDiario
        fields = ['titulo', 'texto']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título da entrada...'}),
            'texto':  forms.Textarea(attrs={'rows': 5, 'placeholder': 'Escreve aqui o teu pensamento...'}),
        }


class FotoAlbumForm(forms.ModelForm):
    class Meta:
        model  = FotoAlbum
        fields = ['imagem', 'legenda']
        widgets = {
            'legenda': forms.TextInput(attrs={'placeholder': 'Legenda (opcional)...'}),
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model  = Perfil
        fields = ['foto_perfil', 'tipo', 'telefone', 'data_nasc']
        widgets = {
            'data_nasc': forms.DateInput(attrs={'type': 'date'}),
            'telefone':  forms.TextInput(attrs={'placeholder': '+351 912 345 678'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Apelido'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'Email'}),
        }