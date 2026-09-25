"""
==============================================================================
ROTEAMENTO DA API RESTFUL (tasks/urls.py)
Responsável pela Implementação: Dev 4 (Controladores e Roteamento)

Orientações para o Dev 4:
  1. Instanciar o DefaultRouter do rest_framework.routers.
  2. Registrar as ViewSets:
     - router.register(r'projetos', ProjetoViewSet, basename='projeto')
     - router.register(r'tarefas', TarefaViewSet, basename='tarefa')
  3. Definir urlpatterns = router.urls.
==============================================================================
"""

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# TODO (Dev 4): Registrar as rotas de 'projetos' e 'tarefas' no router após a criação das ViewSets.

urlpatterns = router.urls
