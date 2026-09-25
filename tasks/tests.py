"""
==============================================================================
SUÍTE DE TESTES AUTOMATIZADOS (tasks/tests.py)
Responsável pela Implementação: Dev 5 (Filtros, Paginação e Testes)

Orientações para o Dev 5:
  1. Implementar testes herdando de rest_framework.test.APITestCase.
  2. Testes obrigatórios:
     - Teste de listagem paginada (GET /api/projetos/ e GET /api/tarefas/).
     - Teste de criação com payload válido (POST -> 201 Created).
     - Teste de validação de regras de negócio (POST inválido -> 400 Bad Request).
     - Teste de consulta detalhada com serialização aninhada (GET /api/projetos/<id>/).
     - Teste de atualização parcial (PATCH /api/tarefas/<id>/ -> 200 OK).
     - Teste de exclusão (DELETE -> 204 No Content).
     - Teste de filtros por status e prioridade.
==============================================================================
"""

from django.test import TestCase
from rest_framework.test import APITestCase

# TODO (Dev 5): Implementar a suíte de testes de integração da API RESTful conforme as orientações acima.
