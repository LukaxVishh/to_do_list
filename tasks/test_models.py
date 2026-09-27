"""Testes da modelagem e das regras de datas do Dev 2."""
from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import PrioridadeTarefa, Projeto, StatusProjeto, Tarefa


class ModelosTests(TestCase):
    def setUp(self):
        self.projeto = Projeto.objects.create(
            nome='Portal', data_inicio=date(2026, 10, 1),
            data_previsao_fim=date(2026, 10, 31),
        )

    def test_defaults_e_relacionamento_reverso(self):
        tarefa = Tarefa.objects.create(projeto=self.projeto, titulo='Desenhar telas')
        tarefa.full_clean()
        self.assertEqual(self.projeto.status, StatusProjeto.PLANEJADO)
        self.assertEqual(tarefa.prioridade, PrioridadeTarefa.MEDIA)
        self.assertFalse(tarefa.concluida)
        self.assertEqual(list(self.projeto.tarefas.all()), [tarefa])
        self.assertIsNotNone(tarefa.criado_em)
        self.assertEqual(str(self.projeto), 'Portal')
        self.assertEqual(str(tarefa), 'Desenhar telas')

    def test_projeto_rejeita_fim_anterior_ao_inicio(self):
        self.projeto.data_previsao_fim = date(2026, 9, 30)
        with self.assertRaises(ValidationError) as erro:
            self.projeto.full_clean()
        self.assertIn('data_previsao_fim', erro.exception.message_dict)

    def test_projeto_aceita_inicio_e_fim_iguais(self):
        self.projeto.data_previsao_fim = self.projeto.data_inicio
        self.projeto.full_clean()

    def test_tarefa_aceita_limites_e_prazo_opcional(self):
        for prazo in (None, date(2026, 10, 1), date(2026, 10, 31)):
            with self.subTest(prazo=prazo):
                Tarefa(projeto=self.projeto, titulo='Tarefa', data_limite=prazo).full_clean()

    def test_tarefa_rejeita_prazo_fora_do_projeto(self):
        for prazo in (date(2026, 9, 30), date(2026, 11, 1)):
            with self.subTest(prazo=prazo):
                tarefa = Tarefa(projeto=self.projeto, titulo='Tarefa', data_limite=prazo)
                with self.assertRaises(ValidationError) as erro:
                    tarefa.full_clean()
                self.assertIn('data_limite', erro.exception.message_dict)

    def test_projeto_obrigatorio_e_fk_invalida(self):
        for projeto_id in (None, self.projeto.pk + 100):
            with self.subTest(projeto_id=projeto_id):
                tarefa = Tarefa(projeto_id=projeto_id, titulo='Tarefa', data_limite=date(2026, 10, 15))
                with self.assertRaises(ValidationError) as erro:
                    tarefa.full_clean()
                self.assertIn('projeto', erro.exception.message_dict)

    def test_exclusao_em_cascata(self):
        tarefa = Tarefa.objects.create(projeto=self.projeto, titulo='Tarefa')
        self.projeto.delete()
        self.assertFalse(Tarefa.objects.filter(pk=tarefa.pk).exists())
