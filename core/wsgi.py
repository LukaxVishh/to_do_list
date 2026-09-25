"""
==============================================================================
CONFIGURAÇÃO WSGI DO PROJETO (core/wsgi.py)
Expõe o callable WSGI como uma variável de módulo chamada 'application'.
==============================================================================
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
