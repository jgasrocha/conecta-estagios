from django.db import models
from django.contrib.auth.models import User
from usuarios.models import PerfilEmpresa 
from datetime import date

class Vaga(models.Model):
    
    MODALIDADE_CHOICES = [
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
    ]

    # Novos status para a gestão
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('analise', 'Em Análise'), # Prazo acabou ou empresa colocou manualmente
        ('finalizada', 'Finalizada/Preenchida'),
    ]

    empresa = models.ForeignKey(PerfilEmpresa, on_delete=models.CASCADE, related_name='vagas')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(verbose_name="Descrição da Vaga")
    requisitos = models.TextField()
    beneficios = models.TextField(blank=True)
    area = models.CharField(max_length=100, verbose_name="Área/Curso")
    
    localizacao = models.CharField(max_length=100, blank=True, null=True)
    modalidade = models.CharField(max_length=20, choices=MODALIDADE_CHOICES, default='presencial')
    
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Bolsa/Salário")
    prazo_candidatura = models.DateField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    # Substituímos o booleano 'ativa' por 'status' para ter mais controle
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')

    def __str__(self):
        return f"{self.titulo} - {self.empresa.nome_empresa}"

    @property
    def is_ativa(self):
        # Verifica se o prazo venceu automaticamente
        if self.status == 'ativa' and self.prazo_candidatura < date.today():
            self.status = 'analise'
            self.save()
            return False
        return self.status == 'ativa'

class Candidatura(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidaturas')
    estudante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='minhas_candidaturas')
    data_candidatura = models.DateTimeField(auto_now_add=True)
    carta_apresentacao = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('vaga', 'estudante')

    def __str__(self):
        return f"{self.estudante.first_name} -> {self.vaga.titulo}"