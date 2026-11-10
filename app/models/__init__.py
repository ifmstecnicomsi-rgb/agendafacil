"""Camada Model: entidades e regras de negócio."""
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ErroValidacao(Exception):
    """Erro de regra de negócio, exibido ao usuário como mensagem amigável."""


# Fuso horário do salão (o servidor de hospedagem roda em UTC)
FUSO = ZoneInfo(os.environ.get("APP_TZ", "America/Sao_Paulo"))


def agora():
    """Data/hora atual no fuso do salão (sem tzinfo, como é gravado no banco)."""
    return datetime.now(FUSO).replace(tzinfo=None)


def formatar_moeda(valor):
    return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def validar_tamanho(texto, maximo, campo):
    if len(texto) > maximo:
        raise ErroValidacao(f"{campo} deve ter no máximo {maximo} caracteres.")


from .usuario import Usuario  # noqa: E402,F401
from .cliente import Cliente  # noqa: E402,F401
from .servico import Servico  # noqa: E402,F401
from .agendamento import Agendamento  # noqa: E402,F401
