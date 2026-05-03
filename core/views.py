from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import RegistoHumor, EntradaDiario, FotoAlbum, Perfil, ReflexaoDia, RelacaoPsicologoPaciente
from .forms import RegistoHumorForm, EntradaDiarioForm, FotoAlbumForm, PerfilForm, UserForm

# ── PAINEL DO PSICÓLOGO ──
@login_required(login_url='login')
def painel_psicologo(request):
    try:
        perfil_obj = request.user.perfil
        if perfil_obj.tipo != 'psicologo':
            return redirect('home')
    except:
        return redirect('home')

    relacoes = RelacaoPsicologoPaciente.objects.filter(
        psicologo=request.user, ativo=True
    ).select_related('paciente')

    return render(request, 'core/psicologo/painel.html', {
        'relacoes': relacoes,
    })


# ── DETALHE DO PACIENTE ──
@login_required(login_url='login')
def detalhe_paciente(request, pk):
    try:
        perfil_obj = request.user.perfil
        if perfil_obj.tipo != 'psicologo':
            return redirect('home')
    except:
        return redirect('home')

    from django.shortcuts import get_object_or_404
    from django.utils import timezone
    from datetime import timedelta

    paciente = get_object_or_404(User, pk=pk)

    # verificar se é mesmo paciente deste psicólogo
    relacao = RelacaoPsicologoPaciente.objects.filter(
        psicologo=request.user, paciente=paciente, ativo=True
    ).first()
    if not relacao:
        return redirect('painel_psicologo')

    # últimos 30 dias de humor
    inicio = timezone.now().date() - timedelta(days=29)
    registos = RegistoHumor.objects.filter(
        utilizador=paciente, data__date__gte=inicio
    ).order_by('data')

    dados_linha = {}
    for r in registos:
        dia = r.data.strftime('%d/%m')
        dados_linha[dia] = r.humor

    from django.db.models import Avg
    media = RegistoHumor.objects.filter(
        utilizador=paciente
    ).aggregate(media=Avg('humor'))['media']

    context = {
        'paciente': paciente,
        'labels': json.dumps(list(dados_linha.keys())),
        'valores': json.dumps(list(dados_linha.values())),
        'media': round(media, 1) if media else None,
        'total_registos': registos.count(),
    }
    return render(request, 'core/psicologo/detalhe_paciente.html', context)


# ── ASSOCIAR PSICÓLOGO ──
@login_required(login_url='login')
def associar_psicologo(request):
    if request.method == 'POST':
        email = request.POST.get('email_psicologo', '').strip()
        try:
            psicologo_user = User.objects.get(email=email)
            if psicologo_user.perfil.tipo != 'psicologo':
                return render(request, 'core/associar_psicologo.html', {
                    'erro': 'Este utilizador não é um psicólogo.'
                })
            RelacaoPsicologoPaciente.objects.get_or_create(
                psicologo=psicologo_user,
                paciente=request.user,
                defaults={'ativo': True}
            )
            return render(request, 'core/associar_psicologo.html', {
                'sucesso': f'Associado com sucesso ao Dr(a). {psicologo_user.first_name} {psicologo_user.last_name}!'
            })
        except User.DoesNotExist:
            return render(request, 'core/associar_psicologo.html', {
                'erro': 'Nenhum utilizador encontrado com esse email.'
            })
    return render(request, 'core/associar_psicologo.html')

# ──────────────────────────────────────────
# PÁGINA INICIAL
# ──────────────────────────────────────────
import random
@login_required(login_url='login')
def home(request):
    from .models import RegistoHumor

    # frases por humor
    frases_por_humor = {
        1: [  # Muito Mau
            ("Após a tempestade vem sempre a bonança. Vai passar. 💛", "Desconhecido"),
            ("É ok não estar bem. Amanhã é um novo dia. 🌅", "Desconhecido"),
            ("A tua dor é válida. Não estás sozinho(a). 💙", "Desconhecido"),
        ],
        2: [  # Mau
            ("Cada dia difícil é um passo para um dia melhor.", "Desconhecido"),
            ("Sê gentil contigo mesmo(a). Estás a fazer o teu melhor. 🌸", "Desconhecido"),
            ("A coragem não é a ausência do medo, mas seguir em frente apesar dele.", "Nelson Mandela"),
        ],
        3: [  # Neutro
            ("A calma é a tua superpotência. 🕊️", "Desconhecido"),
            ("Pequenos progressos são ainda progressos. 🌱", "Desconhecido"),
            ("Hoje é um bom dia para ter um bom dia. ☀️", "Desconhecido"),
        ],
        4: [  # Bom
            ("Continua assim! Estás no bom caminho. 🌟", "Desconhecido"),
            ("A felicidade não é um destino, é uma forma de viajar.", "Margaret Lee Runbeck"),
            ("A tua energia é contagiante. Partilha-a! 😊", "Desconhecido"),
        ],
        5: [  # Muito Bom
            ("Que energia incrível! Aproveita cada momento. 🎉", "Desconhecido"),
            ("A felicidade vem das tuas próprias ações. 🌈", "Dalai Lama"),
            ("És uma inspiração! Continua a brilhar. ✨", "Desconhecido"),
        ],
    }

    # humor de hoje
    from django.utils import timezone
    hoje = timezone.now().date()
    humor_hoje = RegistoHumor.objects.filter(
        utilizador=request.user,
        data__date=hoje
    ).first()

    if humor_hoje:
        frase_lista = frases_por_humor.get(humor_hoje.humor, frases_por_humor[3])
    else:
        frase_lista = frases_por_humor[3]  # neutro se não houver registo

    frase_do_dia = random.choice(frase_lista)

    context = {
        'frase_texto': frase_do_dia[0],
        'frase_autor': frase_do_dia[1],
        'humor_hoje': humor_hoje,
    }
    return render(request, 'core/home.html', context)


# ──────────────────────────────────────────
# REGISTO DE HUMOR
# ──────────────────────────────────────────
@login_required(login_url='login')
def registo_humor(request):
    registos = RegistoHumor.objects.filter(utilizador=request.user)
    if request.method == 'POST':
        form = RegistoHumorForm(request.POST)
        if form.is_valid():
            registo = form.save(commit=False)
            registo.utilizador = request.user
            registo.save()
            return redirect('registo_humor')
    else:
        form = RegistoHumorForm()
    return render(request, 'core/registo_humor.html', {'form': form, 'registos': registos})


# ──────────────────────────────────────────
# DIÁRIO DIGITAL
# ──────────────────────────────────────────
@login_required(login_url='login')
def diario_digital(request):
    entradas = EntradaDiario.objects.filter(utilizador=request.user)
    if request.method == 'POST':
        form = EntradaDiarioForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.utilizador = request.user
            entrada.save()
            return redirect('diario_digital')
    else:
        form = EntradaDiarioForm()
    return render(request, 'core/diario_digital.html', {'form': form, 'entradas': entradas})


@login_required(login_url='login')
def apagar_entrada(request, pk):
    entrada = get_object_or_404(EntradaDiario, pk=pk, utilizador=request.user)
    entrada.delete()
    return redirect('diario_digital')


# ──────────────────────────────────────────
# ÁLBUM
# ──────────────────────────────────────────
@login_required(login_url='login')
def album(request):
    fotos = FotoAlbum.objects.filter(utilizador=request.user)
    if request.method == 'POST':
        form = FotoAlbumForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.utilizador = request.user
            foto.save()
            return redirect('album')
    else:
        form = FotoAlbumForm()
    return render(request, 'core/album.html', {'form': form, 'fotos': fotos})


@login_required(login_url='login')
def apagar_foto(request, pk):
    foto = get_object_or_404(FotoAlbum, pk=pk, utilizador=request.user)
    foto.delete()
    return redirect('album')


# ──────────────────────────────────────────
# EXERCÍCIOS
# ──────────────────────────────────────────
@login_required(login_url='login')
def exercicios(request):
    return render(request, 'core/exercicios.html')


# ──────────────────────────────────────────
# FEELING (frases motivação)
# ──────────────────────────────────────────
@login_required(login_url='login')
def feeling(request):
    return render(request, 'core/feeling.html')


# ──────────────────────────────────────────
# PERFIL
# ──────────────────────────────────────────
from .forms import RegistoHumorForm, EntradaDiarioForm, FotoAlbumForm, PerfilForm, UserForm

@login_required(login_url='login')
def perfil(request):
    perfil_obj, created = Perfil.objects.get_or_create(utilizador=request.user)

    if request.method == 'POST':
        # upload de foto separado
        if 'foto_perfil' in request.FILES:
            perfil_obj.foto_perfil = request.FILES['foto_perfil']
            perfil_obj.save()
            return redirect('perfil')

        # formulário principal
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil_obj)
        user_form   = UserForm(request.POST, instance=request.user)
        if perfil_form.is_valid() and user_form.is_valid():
            perfil_form.save()
            user_form.save()
            # guardar telefone e data_nasc manualmente
            perfil_obj.telefone  = request.POST.get('telefone', '')
            perfil_obj.data_nasc = request.POST.get('data_nasc') or None
            perfil_obj.save()
            return redirect('perfil')
    else:
        perfil_form = PerfilForm(instance=perfil_obj)
        user_form   = UserForm(instance=request.user)

    total_humores = RegistoHumor.objects.filter(utilizador=request.user).count()
    total_diario  = EntradaDiario.objects.filter(utilizador=request.user).count()
    total_fotos   = FotoAlbum.objects.filter(utilizador=request.user).count()

    return render(request, 'core/perfil.html', {
        'perfil_form': perfil_form,
        'user_form':   user_form,
        'perfil':      perfil_obj,
        'total_humores': total_humores,
        'total_diario':  total_diario,
        'total_fotos':   total_fotos,
    })

# ──────────────────────────────────────────
# EERCÍCIOS
# ──────────────────────────────────────────
@login_required(login_url='login')
def respiracao(request):
    return render(request, 'core/exercicios/respiracao.html')

@login_required(login_url='login')
def mindfulness(request):
    return render(request, 'core/exercicios/mindfulness.html')

@login_required(login_url='login')
def relaxamento(request):
    return render(request, 'core/exercicios/relaxamento.html')

@login_required(login_url='login')
def cinco_sentidos(request):
    return render(request, 'core/exercicios/cinco_sentidos.html')


from .models import RegistoHumor, EntradaDiario, FotoAlbum, Perfil, ReflexaoDia


@login_required(login_url='login')
def reflexao_dia(request):
    reflexoes_anteriores = ReflexaoDia.objects.filter(
        utilizador=request.user
    ).order_by('-data')[:10]

    if request.method == 'POST':
        perguntas = [
            "O que correu bem hoje?",
            "O que foi desafiante hoje?",
            "Pelo que estou grato(a) hoje?",
            "O que aprendi hoje?",
            "O que quero melhorar amanhã?",
        ]
        for pergunta in perguntas:
            resposta = request.POST.get(f'resposta_{perguntas.index(pergunta)}', '').strip()
            if resposta:
                ReflexaoDia.objects.create(
                    utilizador=request.user,
                    pergunta=pergunta,
                    resposta=resposta
                )
        return redirect('reflexao_dia')

    return render(request, 'core/exercicios/reflexao.html', {
        'reflexoes_anteriores': reflexoes_anteriores
    })

# ──────────────────────────────────────────
# SIGNUP
# ──────────────────────────────────────────
from .forms import RegistoHumorForm, EntradaDiarioForm, FotoAlbumForm, PerfilForm, UserForm, RegistoForm

def signup(request):
    if request.method == 'POST':
        form = RegistoForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistoForm()
    return render(request, 'core/singup.html', {'form': form})

from django.db.models import Avg
import json

@login_required(login_url='login')
def estatisticas(request):
    from django.utils import timezone
    from datetime import timedelta

    # últimos 30 dias
    hoje = timezone.now().date()
    inicio = hoje - timedelta(days=29)

    registos = RegistoHumor.objects.filter(
        utilizador=request.user,
        data__date__gte=inicio
    ).order_by('data')

    # gráfico de linha — humor por dia
    dados_linha = {}
    for r in registos:
        dia = r.data.strftime('%d/%m')
        dados_linha[dia] = r.humor

    labels = list(dados_linha.keys())
    valores = list(dados_linha.values())

    # humor médio da semana
    semana_inicio = hoje - timedelta(days=6)
    media_semana = RegistoHumor.objects.filter(
        utilizador=request.user,
        data__date__gte=semana_inicio
    ).aggregate(media=Avg('humor'))['media']
    media_semana = round(media_semana, 1) if media_semana else None

    # gráfico circular — % de cada humor
    contagem = {1:0, 2:0, 3:0, 4:0, 5:0}
    for r in registos:
        contagem[r.humor] += 1
    total = sum(contagem.values())

    context = {
        'labels': json.dumps(labels),
        'valores': json.dumps(valores),
        'media_semana': media_semana,
        'contagem_humores': json.dumps(list(contagem.values())),
        'total_registos': total,
    }
    return render(request, 'core/estatisticas.html', context)