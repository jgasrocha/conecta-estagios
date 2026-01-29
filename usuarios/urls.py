from django.urls import path
from . import views

urlpatterns = [
    path('escolha/', views.cadastro_escolha, name='cadastro_escolha'),
    path('cadastro/estudante/', views.cadastro_estudante, name='cadastro_estudante'),
    path('cadastro/empresa/', views.cadastro_empresa, name='cadastro_empresa'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/empresa/', views.perfil_empresa, name='perfil_empresa'),
    path('perfil/estudante/', views.perfil_estudante, name='perfil_estudante'),
    path('perfil/estudante/editar/', views.editar_estudante, name='editar_estudante'),
    path('perfil/empresa/editar/', views.editar_empresa, name='editar_empresa'),
]