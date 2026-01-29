from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed_vagas, name='feed_vagas'),
    path('minhas-vagas/', views.feed_empresa, name='feed_empresa'),
    path('criar/', views.criar_vaga, name='criar_vaga'),
    path('vaga/<int:vaga_id>/', views.detalhe_vaga, name='detalhe_vaga'),
    path('candidatar/<int:vaga_id>/', views.candidatar_vaga, name='candidatar_vaga'),
    path('minhas-candidaturas/', views.historico_candidaturas, name='historico_candidaturas'),
    path('historico/', views.historico_candidaturas, name='historico_candidaturas'),
    path('status/<int:vaga_id>/<str:novo_status>/', views.mudar_status_vaga, name='mudar_status_vaga'),
]