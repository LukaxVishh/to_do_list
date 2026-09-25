"""
==============================================================================
CONFIGURAÇÃO DO APLICATIVO TASKS (tasks/apps.py)
Responsável: Dev 1 (Infraestrutura e Ambiente)
==============================================================================
"""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    verbose_name = 'Gestão de Projetos e Tarefas'
