"""
==============================================================================
ROTEAMENTO PRINCIPAL DO PROJETO (core/urls.py)
Responsável pela Estrutura Base: Dev 1
Descrição:
  - Rota para o painel administrativo do Django (/admin/)
  - Inclusão e delegação das rotas da API RESTful para o app tasks (/api/)
==============================================================================
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Painel administrativo do Django
    path('admin/', admin.site.urls),

    # Delegação dos endpoints da API RESTful para o aplicativo 'tasks'
    path('api/', include('tasks.urls')),
]
