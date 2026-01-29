from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required # <--- Importante adicionar isso
from .forms import UserRegistrationForm, EstudanteProfileForm, EmpresaProfileForm, UserUpdateForm, EmpresaUserUpdateForm

def cadastro_escolha(request):
    return render(request, 'escolha.html')

def cadastro_estudante(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = EstudanteProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            perfil = profile_form.save(commit=False)
            perfil.usuario = user
            perfil.save()
            
            login(request, user)
            return redirect('feed_vagas')
    else:
        user_form = UserRegistrationForm()
        profile_form = EstudanteProfileForm()
    
    return render(request, 'cadastro_estudante.html', {'user_form': user_form, 'profile_form': profile_form})

def cadastro_empresa(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = EmpresaProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            perfil = profile_form.save(commit=False)
            perfil.usuario = user
            perfil.save()
            
            login(request, user)
            return redirect('feed_empresa')
    else:
        user_form = UserRegistrationForm()
        profile_form = EmpresaProfileForm()
    
    return render(request, 'cadastro_empresa.html', {'user_form': user_form, 'profile_form': profile_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if hasattr(user, 'perfil_empresa'):
                return redirect('feed_empresa')
            return redirect('feed_vagas')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def perfil_empresa(request):
    if not hasattr(request.user, 'perfil_empresa'):
        return redirect('feed_vagas')
    
    return render(request, 'perfil_empresa.html')

@login_required
def perfil_estudante(request):
    if hasattr(request.user, 'perfil_empresa'):
        return redirect('feed_empresa')
    
    return render(request, 'perfil_estudante.html')

@login_required
def editar_estudante(request):
    if hasattr(request.user, 'perfil_empresa'):
        return redirect('feed_empresa')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = EstudanteProfileForm(request.POST, request.FILES, instance=request.user.perfil_estudante)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('perfil_estudante')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = EstudanteProfileForm(instance=request.user.perfil_estudante)

    return render(request, 'editar_perfil_estudante.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def editar_empresa(request):
    if not hasattr(request.user, 'perfil_empresa'):
        return redirect('feed_vagas')

    if request.method == 'POST':
        user_form = EmpresaUserUpdateForm(request.POST, instance=request.user)
        profile_form = EmpresaProfileForm(request.POST, request.FILES, instance=request.user.perfil_empresa)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('perfil_empresa')
    else:
        user_form = EmpresaUserUpdateForm(instance=request.user)
        profile_form = EmpresaProfileForm(instance=request.user.perfil_empresa)

    return render(request, 'editar_perfil_empresa.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })