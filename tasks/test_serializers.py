"""Testes das validações expostas pela camada REST (Dev 3)."""
from datetime import date

from django.test import TestCase

from .models import Projeto, Tarefa
from .serializers import ProjetoDetailSerializer, ProjetoSerializer, TarefaSerializer


class SerializersTests(TestCase):
    def setUp(self):
        self.projeto = Projeto.objects.create(
            nome='Portal',
            data_inicio=date(2026, 10, 1),
            data_previsao_fim=date(2026, 10, 31),
        )

    def test_projeto_rejeita_fim_anterior_no_payload(self):
        serializer = ProjetoSerializer(data={
            'nome': 'Inválido',
            'data_inicio': '2026-10-10',
            'data_previsao_fim': '2026-10-05',
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn('data_previsao_fim', serializer.errors)

    def test_tarefa_rejeita_prazo_fora_do_projeto(self):
        serializer = TarefaSerializer(data={
            'projeto': self.projeto.pk,
            'titulo': 'Entrega atrasada',
            'data_limite': '2026-11-01',
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn('data_limite', serializer.errors)

    def test_patch_de_tarefa_revalida_prazo_atual_ao_trocar_projeto(self):
        outro_projeto = Projeto.objects.create(
            nome='Menor',
            data_inicio=date(2026, 10, 1),
            data_previsao_fim=date(2026, 10, 10),
        )
        tarefa = Tarefa.objects.create(
            projeto=self.projeto,
            titulo='Entrega',
            data_limite=date(2026, 10, 20),
        )
        serializer = TarefaSerializer(
            tarefa,
            data={'projeto': outro_projeto.pk},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('data_limite', serializer.errors)

    def test_patch_de_projeto_rejeita_fim_que_invalida_tarefa_existente(self):
        Tarefa.objects.create(
            projeto=self.projeto,
            titulo='Entrega',
            data_limite=date(2026, 10, 20),
        )
        serializer = ProjetoSerializer(
            self.projeto,
            data={'data_previsao_fim': '2026-10-15'},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('data_previsao_fim', serializer.errors)

    def test_patch_de_projeto_rejeita_inicio_que_invalida_tarefa_existente(self):
        Tarefa.objects.create(
            projeto=self.projeto,
            titulo='Planejamento',
            data_limite=date(2026, 10, 10),
        )
        serializer = ProjetoSerializer(
            self.projeto,
            data={'data_inicio': '2026-10-15'},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('data_inicio', serializer.errors)

    def test_detalhe_do_projeto_inclui_tarefas_aninhadas(self):
        tarefa = Tarefa.objects.create(projeto=self.projeto, titulo='Desenhar telas')

        dados = ProjetoDetailSerializer(self.projeto).data

        self.assertEqual(dados['tarefas'][0]['id'], tarefa.pk)
        self.assertEqual(dados['tarefas'][0]['titulo'], 'Desenhar telas')
