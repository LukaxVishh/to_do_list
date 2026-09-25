"""
==============================================================================
CAMADA DE MODELAGEM DE DADOS E PERSISTÊNCIA (tasks/models.py)
Responsável pela Implementação: Dev 2 (Engenharia de Dados e Modelagem ORM)

Orientações para o Dev 2:
  1. Implementar as classes de escolhas (TextChoices) para:
     - StatusProjeto: 'PLANEJADO', 'EM_ANDAMENTO', 'CONCLUIDO', 'CANCELADO'
     - PrioridadeTarefa: 'BAIXA', 'MEDIA', 'ALTA'
  2. Implementar a classe 'Projeto':
     - Campos: nome (CharField), descricao (TextField), data_inicio (DateField),
       data_previsao_fim (DateField), status (CharField com choices), criado_em e atualizado_em.
     - Validação clean(): data_previsao_fim não pode ser anterior a data_inicio.
  3. Implementar a classe 'Tarefa':
     - Relacionamento explícito 1:N via models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='tarefas').
     - Campos: titulo (CharField), descricao (TextField), prioridade (CharField com choices),
       concluida (BooleanField), data_limite (DateField), criado_em e atualizado_em.
     - Validação clean(): data_limite não pode ser anterior a data_inicio do projeto associado.
  4. Executar 'python manage.py makemigrations tasks' e 'python manage.py migrate'.
==============================================================================
"""

from django.db import models
from django.core.exceptions import ValidationError

# TODO (Dev 2): Implementar os modelos Projeto e Tarefa conforme as orientações acima.
