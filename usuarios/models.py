from django.db import models
from django.contrib.auth.models import User

class PerfilEstudante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_estudante')
    nome_completo = models.CharField(max_length=150, blank=True)
    telefone = models.CharField(max_length=20)
    instituicao = models.CharField(max_length=100, verbose_name="Instituição de Ensino")
    curso = models.CharField(max_length=100)
    semestre = models.PositiveIntegerField(default=1)
    foto = models.ImageField(upload_to='fotos_estudantes/', null=True, blank=True)
    curriculo = models.FileField(upload_to='curriculos/', null=True, blank=True)
    habilidades = models.TextField(blank=True, help_text="Liste suas habilidades separadas por vírgula")
    
    def __str__(self):
        return f"Estudante: {self.nome_completo}"

class PerfilEmpresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_empresa')
    nome_empresa = models.CharField(max_length=100) # Nome fantasia
    cnpj = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20)
    descricao = models.TextField(blank=True, verbose_name="Sobre a Empresa")
    logo = models.ImageField(upload_to='logos_empresas/', null=True, blank=True)

    def __str__(self):
        return self.nome_empresa