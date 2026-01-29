from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Função simples para redirecionar a raiz (/) para o login
def home_redirect(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'), # Redireciona www.site.com para o login
    path('usuarios/', include('usuarios.urls')),
    path('vagas/', include('vagas.urls')),
] 

# Isso permite servir os arquivos de media (currículos/fotos) em modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)