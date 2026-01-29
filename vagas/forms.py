from django import forms
from .models import Vaga, Candidatura

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        exclude = ['empresa', 'data_publicacao', 'ativa', 'status']
        
        widgets = {
            'prazo_candidatura': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'requisitos': forms.Textarea(attrs={'rows': 4}),
            'beneficios': forms.Textarea(attrs={'rows': 4}),
        }

class CandidaturaForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = ['carta_apresentacao']
        widgets = {
            'carta_apresentacao': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Escreva uma breve apresentação...'}),
        }