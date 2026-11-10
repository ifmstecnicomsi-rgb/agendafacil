import os
import sys
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402
from app.config import TestConfig  # noqa: E402
from app.models import Cliente, Servico, db  # noqa: E402


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logado(client):
    client.post("/login", data={"email": "admin@agendafacil.com", "senha": "admin123"})
    return client


@pytest.fixture
def cliente(app):
    c = Cliente()
    c.preencher("Maria Souza", "(61) 99999-1234", "maria@email.com")
    db.session.add(c)
    db.session.commit()
    return c


@pytest.fixture
def servico(app):
    s = Servico()
    s.preencher("Corte feminino", 60, "80,00")
    db.session.add(s)
    db.session.commit()
    return s


def proximo_dia_util(hora=10, minuto=0):
    """Retorna um horário futuro de segunda a sábado."""
    d = datetime.now() + timedelta(days=2)
    while d.weekday() == 6:
        d += timedelta(days=1)
    return d.replace(hour=hora, minute=minuto, second=0, microsecond=0)
