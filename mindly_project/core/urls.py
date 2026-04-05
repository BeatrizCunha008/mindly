from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # página inicial
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),

    # páginas internas
    path('registo-humor/', views.registo_humor, name='registo_humor'),
    path('diario-digital/', views.diario_digital, name='diario_digital'),
    path('exercicios/', views.exercicios, name='exercicios'),
    path('album/', views.album, name='album'),
    path('feeling/', views.feeling, name='feeling'),
]
