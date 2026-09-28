"""Testes de integração dos endpoints REST (Dev 5)."""
from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Projeto, Tarefa


class ProjetoEndpointTests(APITestCase):
    def setUp(self):
        self.projeto = Projeto.objects.create(
            nome='Portal institucional',
            descricao='Modernização do portal',
            data_inicio=date(2026, 10, 1),
            data_previsao_fim=date(2026, 10, 31),
            status='PLANEJADO',
        )

    def payload_projeto(self, **overrides):
        payload = {
            'nome': 'Aplicativo mobile',
            'descricao': 'Aplicativo para clientes',
            'data_inicio': '2026-11-01',
            'data_previsao_fim': '2026-11-30',
            'status': 'EM_ANDAMENTO',
        }
        payload.update(overrides)
        return payload

    def test_crud_de_projeto_e_detalhe_com_tarefas_aninhadas(self):
        create_response = self.client.post(
            reverse('projeto-list'), self.payload_projeto(), format='json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        projeto_id = create_response.data['id']

        tarefa = Tarefa.objects.create(
            projeto_id=projeto_id,
            titulo='Implementar autenticação',
            data_limite=date(2026, 11, 10),
        )
        detail_url = reverse('projeto-detail', args=[projeto_id])
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['tarefas'][0]['id'], tarefa.id)

        update_response = self.client.patch(
            detail_url, {'status': 'CONCLUIDO'}, format='json'
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['status'], 'CONCLUIDO')

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Projeto.objects.filter(pk=projeto_id).exists())
        self.assertFalse(Tarefa.objects.filter(pk=tarefa.id).exists())

    def test_projeto_rejeita_payload_com_datas_incoerentes(self):
        response = self.client.post(
            reverse('projeto-list'),
            self.payload_projeto(
                data_inicio='2026-11-30', data_previsao_fim='2026-11-01'
            ),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data_previsao_fim', response.data)

    def test_lista_projetos_e_paginada_filtrada_buscada_e_ordenada(self):
        for index in range(10):
            inicio = date(2026, 12, 1) + timedelta(days=index)
            Projeto.objects.create(
                nome=f'Projeto {index}',
                data_inicio=inicio,
                data_previsao_fim=inicio + timedelta(days=5),
                status='CONCLUIDO' if index == 0 else 'PLANEJADO',
            )

        response = self.client.get(reverse('projeto-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

        filtered = self.client.get(reverse('projeto-list'), {'status': 'CONCLUIDO'})
        self.assertEqual(filtered.data['count'], 1)
        self.assertEqual(filtered.data['results'][0]['status'], 'CONCLUIDO')

        searched = self.client.get(reverse('projeto-list'), {'search': 'institucional'})
        self.assertEqual(searched.data['count'], 1)
        self.assertEqual(searched.data['results'][0]['id'], self.projeto.id)

        ordered = self.client.get(reverse('projeto-list'), {'ordering': '-data_inicio'})
        datas = [item['data_inicio'] for item in ordered.data['results']]
        self.assertEqual(datas, sorted(datas, reverse=True))


class TarefaEndpointTests(APITestCase):
    def setUp(self):
        self.projeto = Projeto.objects.create(
            nome='Projeto base',
            data_inicio=date(2026, 10, 1),
            data_previsao_fim=date(2026, 10, 31),
        )
        self.outro_projeto = Projeto.objects.create(
            nome='Outro projeto',
            data_inicio=date(2026, 11, 1),
            data_previsao_fim=date(2026, 11, 30),
        )

    def payload_tarefa(self, **overrides):
        payload = {
            'projeto': self.projeto.id,
            'titulo': 'Implementar API',
            'descricao': 'Criar endpoints REST',
            'prioridade': 'ALTA',
            'concluida': False,
            'data_limite': '2026-10-15',
        }
        payload.update(overrides)
        return payload

    def test_crud_de_tarefa(self):
        create_response = self.client.post(
            reverse('tarefa-list'), self.payload_tarefa(), format='json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        tarefa_id = create_response.data['id']

        detail_url = reverse('tarefa-detail', args=[tarefa_id])
        patch_response = self.client.patch(
            detail_url, {'concluida': True}, format='json'
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertTrue(patch_response.data['concluida'])

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tarefa.objects.filter(pk=tarefa_id).exists())

    def test_lista_tarefas_e_paginada(self):
        for index in range(11):
            Tarefa.objects.create(
                projeto=self.projeto,
                titulo=f'Tarefa {index}',
                data_limite=date(2026, 10, 15),
            )

        response = self.client.get(reverse('tarefa-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_lista_tarefas_aplica_filtros_e_busca_por_titulo(self):
        tarefa = Tarefa.objects.create(
            projeto=self.projeto,
            titulo='Corrigir API de pagamentos',
            prioridade='ALTA',
            concluida=False,
            data_limite=date(2026, 10, 10),
        )
        Tarefa.objects.create(
            projeto=self.outro_projeto,
            titulo='Escrever documentação',
            prioridade='BAIXA',
            concluida=True,
            data_limite=date(2026, 11, 10),
        )

        for params in (
            {'prioridade': 'ALTA'},
            {'concluida': 'false'},
            {'projeto': self.projeto.id},
            {'search': 'pagamentos'},
        ):
            with self.subTest(params=params):
                response = self.client.get(reverse('tarefa-list'), params)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['count'], 1)
                self.assertEqual(response.data['results'][0]['id'], tarefa.id)
