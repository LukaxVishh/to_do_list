"""Administração de projetos e tarefas (Dev 2)."""
from django.contrib import admin
from .models import Projeto, Tarefa


class TarefaInline(admin.TabularInline):
    model = Tarefa
    extra = 1
    fields = ['titulo', 'descricao', 'prioridade', 'concluida', 'data_limite']


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'status', 'data_inicio', 'data_previsao_fim', 'criado_em']
    list_filter = ['status']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [TarefaInline]


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'projeto', 'prioridade', 'concluida', 'data_limite']
    list_filter = ['prioridade', 'concluida', 'projeto']
    search_fields = ['titulo', 'descricao', 'projeto__nome']
    readonly_fields = ['criado_em', 'atualizado_em']
    list_select_related = ['projeto']
