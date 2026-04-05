from django.db import models
from django.contrib.auth.models import User


# ──────────────────────────────────────────
# PERFIL DO UTILIZADOR (com tipo)
# ──────────────────────────────────────────
class Perfil(models.Model):
    TIPO_CHOICES = [
        ('livre',      'Utilizador Livre'),
        ('paciente',   'Paciente'),
        ('psicologo',  'Psicólogo'),
    ]

    utilizador  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo        = models.CharField(max_length=20, choices=TIPO_CHOICES, default='livre')
    foto_perfil = models.ImageField(upload_to='perfis/', blank=True, null=True)
    bio         = models.TextField(blank=True, null=True)
    telefone    = models.CharField(max_length=20, blank=True, null=True)
    data_nasc   = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.utilizador.username} ({self.get_tipo_display()})"

    def is_psicologo(self):
        return self.tipo == 'psicologo'

    def is_paciente(self):
        return self.tipo == 'paciente'


# ──────────────────────────────────────────
# RELAÇÃO PSICÓLOGO ↔ PACIENTE
# ──────────────────────────────────────────
class RelacaoPsicologoPaciente(models.Model):
    psicologo = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='pacientes', limit_choices_to={'perfil__tipo': 'psicologo'}
    )
    paciente  = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='psicologos', limit_choices_to={'perfil__tipo': 'paciente'}
    )
    data_associacao = models.DateTimeField(auto_now_add=True)
    ativo           = models.BooleanField(default=True)

    class Meta:
        unique_together = ('psicologo', 'paciente')

    def __str__(self):
        return f"Dr(a). {self.psicologo.username} → {self.paciente.username}"


# ──────────────────────────────────────────
# REGISTO DE HUMOR
# ──────────────────────────────────────────
class RegistoHumor(models.Model):
    HUMOR_CHOICES = [
        (1, 'Muito Mau 😢'),
        (2, 'Mau 😕'),
        (3, 'Neutro 😐'),
        (4, 'Bom 🙂'),
        (5, 'Muito Bom 😄'),
    ]

    utilizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registos_humor')
    humor      = models.IntegerField(choices=HUMOR_CHOICES)
    nota       = models.TextField(blank=True, null=True)
    data       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"{self.utilizador.username} — {self.get_humor_display()} ({self.data.strftime('%d/%m/%Y')})"


# ──────────────────────────────────────────
# DIÁRIO DIGITAL
# ──────────────────────────────────────────
class EntradaDiario(models.Model):
    utilizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entradas_diario')
    titulo     = models.CharField(max_length=200)
    texto      = models.TextField()
    data       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"{self.utilizador.username} — {self.titulo} ({self.data.strftime('%d/%m/%Y')})"


# ──────────────────────────────────────────
# ÁLBUM DE FOTOS
# ──────────────────────────────────────────
class FotoAlbum(models.Model):
    utilizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fotos_album')
    imagem     = models.ImageField(upload_to='album/')
    legenda    = models.CharField(max_length=300, blank=True, null=True)
    data       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"{self.utilizador.username} — foto ({self.data.strftime('%d/%m/%Y')})"


# ──────────────────────────────────────────
# EXERCÍCIOS
# ──────────────────────────────────────────
class Exercicio(models.Model):
    TIPO_CHOICES = [
        ('respiracao',  'Respiração'),
        ('mindfulness', 'Mindfulness'),
        ('relaxamento', 'Relaxamento Muscular'),
        ('sentidos',    '5 Sentidos'),
        ('reflexao',    'Reflexão do Dia'),
    ]

    nome      = models.CharField(max_length=200)
    tipo      = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descricao = models.TextField()
    audio     = models.FileField(upload_to='audios/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.nome}"


# ──────────────────────────────────────────
# FRASES MOTIVACIONAIS
# ──────────────────────────────────────────
class FraseMotivacional(models.Model):
    texto                 = models.TextField()
    data_disponibilizacao = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.texto[:60]


# ──────────────────────────────────────────
# RELATÓRIO (modo profissional)
# ──────────────────────────────────────────
class Relatorio(models.Model):
    PERIODO_CHOICES = [
        ('semanal', 'Semanal'),
        ('mensal',  'Mensal'),
    ]

    paciente     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relatorios')
    psicologo    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relatorios_gerados')
    periodo      = models.CharField(max_length=20, choices=PERIODO_CHOICES, default='semanal')
    data_inicio  = models.DateField()
    data_fim     = models.DateField()
    estatisticas = models.JSONField(default=dict)
    criado_em    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"Relatório {self.get_periodo_display()} — {self.paciente.username} ({self.data_inicio} a {self.data_fim})"


# ──────────────────────────────────────────
# REFLEXÃO DO DIA
# ──────────────────────────────────────────
class ReflexaoDia(models.Model):
    utilizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reflexoes')
    pergunta   = models.CharField(max_length=300)
    resposta   = models.TextField()
    data       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"{self.utilizador.username} — {self.pergunta[:40]} ({self.data.strftime('%d/%m/%Y')})"