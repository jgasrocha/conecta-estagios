from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .models import Vaga, Candidatura
from .forms import VagaForm, CandidaturaForm

@login_required
def feed_vagas(request):
    # Antes de listar, verifica se alguma vaga venceu hoje (atualização 'lazy')
    # Isso garante que o aluno só veja vagas que realmente estão no prazo
    vagas_ativas = Vaga.objects.filter(status='ativa')
    
    for vaga in vagas_ativas:
        # A propriedade .is_ativa que criamos no model já atualiza o status se venceu
        vaga.is_ativa 

    # Agora busca apenas as que continuam ativas
    vagas = Vaga.objects.filter(status='ativa').order_by('-data_publicacao')

    query = request.GET.get('q') # Pega o texto do input name="q"
    if query:
        # Filtra por Título OU Nome da Empresa OU Localização OU Área
        vagas = vagas.filter(
            Q(titulo__icontains=query) |
            Q(empresa__nome_empresa__icontains=query) |
            Q(localizacao__icontains=query) |
            Q(area__icontains=query)
        )
    return render(request, 'feed_estudante.html', {'vagas': vagas})

@login_required
def feed_empresa(request):
    if not hasattr(request.user, 'perfil_empresa'):
        return redirect('feed_vagas')
        
    vagas = Vaga.objects.filter(empresa=request.user.perfil_empresa).order_by('-data_publicacao')

    query = request.GET.get('q')
    if query:
        # Filtra por Título OU Área (case insensitive)
        vagas = vagas.filter(
            Q(titulo__icontains=query) | 
            Q(area__icontains=query)
        )
    # Atualiza status de vagas vencidas ao carregar o painel da empresa
    for vaga in vagas:
        vaga.is_ativa 

    return render(request, 'feed_empresa.html', {'vagas': vagas})

@login_required
def criar_vaga(request):
    if not hasattr(request.user, 'perfil_empresa'):
        return redirect('feed_vagas')

    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user.perfil_empresa
            
            vaga.status = 'ativa' 
            
            vaga.save()
            return redirect('feed_empresa')
        else:
            print(form.errors) 
    else:
        form = VagaForm()
    
    return render(request, 'criarvaga.html', {'form': form})

@login_required
def detalhe_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    vaga.is_ativa 

    ja_candidatou = False
    is_owner = False
    candidatos = []

    if hasattr(request.user, 'perfil_empresa') and vaga.empresa == request.user.perfil_empresa:
        is_owner = True
        candidatos = vaga.candidaturas.select_related('estudante', 'estudante__perfil_estudante').order_by('-data_candidatura')

    elif request.user.is_authenticated and hasattr(request.user, 'perfil_estudante'):
        ja_candidatou = Candidatura.objects.filter(vaga=vaga, estudante=request.user).exists()
        
    return render(request, 'visualizar.html', {
        'vaga': vaga, 
        'ja_candidatou': ja_candidatou,
        'is_owner': is_owner,     
        'candidatos': candidatos 
    })

@login_required
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    # Impede candidatura se a vaga não estiver ativa
    if vaga.status != 'ativa':
        return redirect('feed_vagas') # Ou uma página de erro

    if request.method == 'POST':
        form = CandidaturaForm(request.POST)
        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.vaga = vaga
            candidatura.estudante = request.user
            candidatura.save()
            return redirect('feed_vagas')
    else:
        form = CandidaturaForm()
        
    return render(request, 'candidatar.html', {'vaga': vaga, 'form': form})

# --- NOVA FUNÇÃO: Histórico do Estudante ---
@login_required
def historico_candidaturas(request):
    if hasattr(request.user, 'perfil_empresa'):
        return redirect('feed_empresa')

    candidaturas = (
        Candidatura.objects
        .filter(estudante=request.user)
        .select_related('vaga', 'vaga__empresa')
        .order_by('-data_candidatura')
    )

    return render(request, 'historico_candidaturas.html', {'candidaturas': candidaturas})

# --- NOVA FUNÇÃO: Gestão de Status pela Empresa ---
@login_required
def mudar_status_vaga(request, vaga_id, novo_status):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    # Segurança: garante que a vaga pertence à empresa logada
    if not hasattr(request.user, 'perfil_empresa') or vaga.empresa != request.user.perfil_empresa:
        return redirect('feed_vagas')
    
    if novo_status in ['ativa', 'analise', 'finalizada']:
        vaga.status = novo_status
        vaga.save()
        
    return redirect('feed_empresa')