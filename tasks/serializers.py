"""
==============================================================================
CAMADA DE SERIALIZAÇÃO E VALIDAÇÕES (tasks/serializers.py)
Responsável pela Implementação: Dev 3 (Serializadores e Validações)

Orientações para o Dev 3:
  1. Implementar 'TarefaSerializer' (serializers.ModelSerializer):
     - Validar que data_limite não seja anterior à data de início do projeto pai.
  2. Implementar 'TarefaNestedSerializer' (serializers.ModelSerializer):
     - Serializador simplificado para leitura de tarefas aninhadas dentro do Projeto.
  3. Implementar 'ProjetoSerializer' (serializers.ModelSerializer):
     - Incluir validação no método validate(): data_previsao_fim >= data_inicio.
     - (Opcional) Incluir contadores computados como total_tarefas.
  4. Implementar 'ProjetoDetailSerializer' (herda de ProjetoSerializer):
     - Incluir campo de serialização aninhada: tarefas = TarefaNestedSerializer(many=True, read_only=True).
==============================================================================
"""

from rest_framework import serializers

# TODO (Dev 3): Implementar TarefaSerializer, ProjetoSerializer e ProjetoDetailSerializer conforme as orientações acima.
