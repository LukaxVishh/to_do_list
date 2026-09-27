"""Modelos de projetos e tarefas (Dev 2)."""
from django.core.exceptions import ValidationError
from django.db import models


class StatusProjeto(models.TextChoices):
    PLANEJADO = 'PLANEJADO', 'Planejado'
    EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em andamento'
    CONCLUIDO = 'CONCLUIDO', 'Concluído'
    CANCELADO = 'CANCELADO', 'Cancelado'


class PrioridadeTarefa(models.TextChoices):
    BAIXA = 'BAIXA', 'Baixa'
    MEDIA = 'MEDIA', 'Média'
    ALTA = 'ALTA', 'Alta'


class Projeto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(null=True, blank=True)
    data_inicio = models.DateField()
    data_previsao_fim = models.DateField()
    status = models.CharField(max_length=12, choices=StatusProjeto.choices, default=StatusProjeto.PLANEJADO)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if self.data_inicio and self.data_previsao_fim and self.data_previsao_fim < self.data_inicio:
            raise ValidationError({'data_previsao_fim': 'A data de previsão de término não pode ser anterior à data de início do projeto.'})


class Tarefa(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='tarefas')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)
    prioridade = models.CharField(max_length=5, choices=PrioridadeTarefa.choices, default=PrioridadeTarefa.MEDIA)
    concluida = models.BooleanField(default=False)
    data_limite = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        if self.data_limite is None:
            return
        try:
            projeto = self.projeto
        except Projeto.DoesNotExist:
            # A validação do campo informa uma FK ausente ou inválida.
            return
        if projeto.data_inicio and self.data_limite < projeto.data_inicio:
            raise ValidationError({'data_limite': 'O prazo da tarefa não pode ser anterior ao início do projeto.'})
        if projeto.data_previsao_fim and self.data_limite > projeto.data_previsao_fim:
            raise ValidationError({'data_limite': 'O prazo da tarefa não pode ser posterior ao término previsto do projeto.'})
