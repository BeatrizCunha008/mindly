from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # autenticação
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),

    # páginas internas
    path('registo-humor/', views.registo_humor, name='registo_humor'),
    path('diario-digital/', views.diario_digital, name='diario_digital'),
    path('diario-digital/apagar/<int:pk>/', views.apagar_entrada, name='apagar_entrada'),
    path('exercicios/', views.exercicios, name='exercicios'),
    path('exercicios/respiracao/', views.respiracao, name='respiracao'),
    path('exercicios/mindfulness/', views.mindfulness, name='mindfulness'),
    path('exercicios/relaxamento/', views.relaxamento, name='relaxamento'),
    path('exercicios/5sentidos/', views.cinco_sentidos, name='cinco_sentidos'),
    path('exercicios/reflexao/', views.reflexao_dia, name='reflexao_dia'),
    path('album/', views.album, name='album'),
    path('album/apagar/<int:pk>/', views.apagar_foto, name='apagar_foto'),
    path('feeling/', views.feeling, name='feeling'),
    path('perfil/', views.perfil, name='perfil'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('psicologo/', views.painel_psicologo, name='painel_psicologo'),
    path('psicologo/paciente/<int:pk>/', views.detalhe_paciente, name='detalhe_paciente'),
    path('associar-psicologo/', views.associar_psicologo, name='associar_psicologo'),
]