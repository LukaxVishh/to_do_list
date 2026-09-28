"""
==============================================================================
CAMADA DE VISÃO E CONTROLADORES (tasks/views.py)
Responsáveis pela Implementação:
  - Dev 4: Controladores RESTful (ModelViewSet, get_serializer_class)
  - Dev 5: Configuração de Filtros, Busca Textual e Ordenação

Orientações para o Dev 4:
  1. Implementar 'ProjetoViewSet' herdando de viewsets.ModelViewSet:
     - queryset = Projeto.objects.all()
     - Sobrescrever get_serializer_class() para retornar ProjetoDetailSerializer no 'retrieve'
       e ProjetoSerializer nas demais ações.
  2. Implementar 'TarefaViewSet' herdando de viewsets.ModelViewSet:
     - queryset = Tarefa.objects.all()
     - serializer_class = TarefaSerializer

Orientações para o Dev 5:
  1. Configurar em 'ProjetoViewSet':
     - filterset_fields = ['status']
     - search_fields = ['nome', 'descricao']
     - ordering_fields = ['data_inicio', 'data_previsao_fim', 'criado_em']
  2. Configurar em 'TarefaViewSet':
     - filterset_fields = ['prioridade', 'concluida', 'projeto']
     - search_fields = ['titulo', 'descricao']
     - ordering_fields = ['data_limite', 'prioridade', 'criado_em']
==============================================================================
"""

from rest_framework import viewsets

from .models import Projeto, Tarefa
from .serializers import ProjetoDetailSerializer, ProjetoSerializer, TarefaSerializer


class ProjetoViewSet(viewsets.ModelViewSet):
    """Expõe CRUD, filtro, busca e ordenação de projetos."""

    queryset = Projeto.objects.all()
    filterset_fields = ['status']
    search_fields = ['nome']
    ordering_fields = ['data_inicio']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjetoDetailSerializer
        return ProjetoSerializer


class TarefaViewSet(viewsets.ModelViewSet):
    """Expõe CRUD, filtros e busca de tarefas."""

    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    filterset_fields = ['prioridade', 'concluida', 'projeto']
    search_fields = ['titulo']
