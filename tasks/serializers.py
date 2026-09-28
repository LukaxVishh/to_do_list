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

from .models import Projeto, Tarefa


class TarefaSerializer(serializers.ModelSerializer):
    """Serializa tarefas e garante que seu prazo pertença ao projeto."""

    class Meta:
        model = Tarefa
        fields = [
            'id',
            'projeto',
            'titulo',
            'descricao',
            'prioridade',
            'concluida',
            'data_limite',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def validate(self, attrs):
        """Também valida PATCHes, combinando o payload com a instância atual."""
        projeto = attrs.get('projeto', getattr(self.instance, 'projeto', None))
        data_limite = attrs.get('data_limite', getattr(self.instance, 'data_limite', None))

        if projeto is None or data_limite is None:
            return attrs

        if data_limite < projeto.data_inicio:
            raise serializers.ValidationError({
                'data_limite': 'O prazo da tarefa não pode ser anterior ao início do projeto.'
            })
        if data_limite > projeto.data_previsao_fim:
            raise serializers.ValidationError({
                'data_limite': 'O prazo da tarefa não pode ser posterior ao término previsto do projeto.'
            })

        return attrs


class TarefaNestedSerializer(TarefaSerializer):
    """Representação de leitura usada dentro do detalhe de um projeto."""

    class Meta(TarefaSerializer.Meta):
        read_only_fields = TarefaSerializer.Meta.fields


class ProjetoSerializer(serializers.ModelSerializer):
    """Serializa projetos e valida a coerência do cronograma."""

    class Meta:
        model = Projeto
        fields = [
            'id',
            'nome',
            'descricao',
            'data_inicio',
            'data_previsao_fim',
            'status',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def validate(self, attrs):
        """Valida criação e atualização parcial sem ignorar os dados persistidos."""
        data_inicio = attrs.get('data_inicio', getattr(self.instance, 'data_inicio', None))
        data_previsao_fim = attrs.get(
            'data_previsao_fim',
            getattr(self.instance, 'data_previsao_fim', None),
        )

        if (
            data_inicio is not None
            and data_previsao_fim is not None
            and data_previsao_fim < data_inicio
        ):
            raise serializers.ValidationError({
                'data_previsao_fim': (
                    'A data de previsão de término não pode ser anterior à data de início do projeto.'
                )
            })

        if self.instance is not None:
            tarefas = self.instance.tarefas.exclude(data_limite__isnull=True)
            erros = {}
            if tarefas.filter(data_limite__lt=data_inicio).exists():
                erros['data_inicio'] = (
                    'A nova data de início deixaria tarefas existentes com prazo anterior ao projeto.'
                )
            if tarefas.filter(data_limite__gt=data_previsao_fim).exists():
                erros['data_previsao_fim'] = (
                    'A nova data de término deixaria tarefas existentes com prazo posterior ao projeto.'
                )
            if erros:
                raise serializers.ValidationError(erros)

        return attrs


class ProjetoDetailSerializer(ProjetoSerializer):
    """Acrescenta as tarefas ao consultar um projeto individualmente."""

    tarefas = TarefaNestedSerializer(many=True, read_only=True)

    class Meta(ProjetoSerializer.Meta):
        fields = ProjetoSerializer.Meta.fields + ['tarefas']
