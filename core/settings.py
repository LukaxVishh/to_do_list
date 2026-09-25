"""
==============================================================================
CONFIGURAÇÕES DO PROJETO DJANGO (settings.py)
Responsável pela Implementação: Dev 1 (Infraestrutura e Ambiente)
Descrição:
  - Gerenciamento de variáveis sensíveis via python-dotenv (.env)
  - Registro de apps de terceiros (rest_framework, django_filters) e apps locais (tasks)
  - Configuração de internacionalização e fuso horário brasileiro
  - Configuração global do Django REST Framework (paginação e filtros padrão)
==============================================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Diretório base do projeto (to_do_list/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Carregamento do arquivo .env com tratamento de variáveis de ambiente
load_dotenv(BASE_DIR / '.env')

# Chave de segurança obtida a partir do .env com valor de fallback para desenvolvimento
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-chave-padrao-fallback-desenvolvimento')

# Modo de depuração obtido via .env (converte string para booleano)
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')

# Lista de hosts permitidos lidos do .env e convertidos em lista
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
    if host.strip()
]


# Definição dos Aplicativos Instalados no Projeto
INSTALLED_APPS = [
    # Aplicativos nativos do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Bibliotecas e Frameworks de terceiros
    'rest_framework',
    'django_filters',

    # Aplicativos modulares do domínio da aplicação
    'tasks.apps.TasksConfig',
]

# Middlewares responsáveis pelo fluxo de requisição/resposta HTTP
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Módulo de rotas principal do projeto
ROOT_URLCONF = 'core.urls'

# Configuração de templates do Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração de execução da aplicação WSGI
WSGI_APPLICATION = 'core.wsgi.application'


# Configuração do Banco de Dados Relacional (SQLite padrão para desenvolvimento)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validadores de senha padrão do Django Auth
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalização e Localização
# Idioma em Português Brasileiro e Fuso Horário de Brasília
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# Arquivos Estáticos (CSS, JavaScript, Imagens)
STATIC_URL = 'static/'

# Tipo padrão de chave primária para os modelos ORM
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# CONFIGURAÇÕES GLOBAIS DO DJANGO REST FRAMEWORK (DRF)
# ==============================================================================
REST_FRAMEWORK = {
    # Habilita a paginação nativa por padrão em todas as listas de recursos
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    # Define os backends padrão para processamento de filtros, busca e ordenação
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
