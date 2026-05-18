import os
import django
import sys
from pathlib import Path

# Add project paths to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
novo_backend = project_root / "novo" / "backend"

sys.path.insert(0, str(novo_backend))
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.django_settings")

try:
    django.setup()
except RuntimeError:
    pass  # Django already configured

import pytest
from django.test import Client
from django.db import connection
from django.test.utils import CaptureQueriesContext

@pytest.fixture
def api_client():
    """Django test client for HTTP requests."""
    return Client()

@pytest.fixture
def db_setup(db):
    """Setup database before tests."""
    # Database is already created by pytest-django
    return db

@pytest.fixture(autouse=True)
def reset_sequences(db):
    """Reset database sequences after each test."""
    yield
    if hasattr(connection, 'queries'):
        connection.queries_log.clear()
