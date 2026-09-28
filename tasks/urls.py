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

from .views import ProjetoViewSet, TarefaViewSet


router = DefaultRouter()

router.register(r'projetos', ProjetoViewSet, basename='projeto')
router.register(r'tarefas', TarefaViewSet, basename='tarefa')

urlpatterns = router.urls
