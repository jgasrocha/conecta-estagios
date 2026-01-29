from django import forms
from django.contrib.auth.models import User
from .models import PerfilEstudante, PerfilEmpresa

# Formulário para criar o Usuário básico
class UserRegistrationForm(forms.ModelForm):
    # Definindo label manualmente para garantir tradução
    username = forms.CharField(label="Usuário")
    email = forms.EmailField(label="E-mail")  # <--- AQUI A CORREÇÃO
    
    senha = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput()
    )
    confirmar_senha = forms.CharField(
        label="Confirmar Senha", 
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        # Removemos 'password' para não duplicar e mantemos username e email
        # O label definido acima sobrescreve o padrão do model
        fields = ['username', 'email'] 

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', "As senhas não conferem.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["senha"])
        if commit:
            user.save()
        return user

# ... restante dos formulários (EstudanteProfileForm, EmpresaProfileForm, etc.) permanece igual ...
class EstudanteProfileForm(forms.ModelForm):
    class Meta:
        model = PerfilEstudante
        fields = ['foto', 'telefone', 'instituicao', 'curso', 'semestre', 'habilidades', 'curriculo']
        labels = {
            'instituicao': 'Instituição de Ensino',
            'foto': 'Foto de Perfil'
        }

class EmpresaProfileForm(forms.ModelForm):
    class Meta:
        model = PerfilEmpresa
        fields = ['nome_empresa', 'cnpj', 'telefone', 'descricao', 'logo']
        labels = {
            'nome_empresa': 'Nome da Empresa',
            'descricao': 'Sobre a Empresa'
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="E-mail") # Garante no update também
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome'
        }

class EmpresaUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="E-mail")
    class Meta:
        model = User
        fields = ['email']