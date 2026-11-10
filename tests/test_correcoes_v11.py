"""Testes de regressão dos erros encontrados nos testes exploratórios (versão 1.1)."""
import os
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from app.models import (Agendamento, Cliente, ErroValidacao, Servico, Usuario, agora, db,
                        formatar_moeda)
from conftest import proximo_dia_util


# E01 – cadastro público
def test_e01_visitante_nao_cadastra_usuario(client):
    r = client.post("/cadastro", data={"nome": "Intruso", "email": "intruso@x.com",
                                       "senha": "123456", "confirmar": "123456"})
    assert r.status_code == 302 and "/login" in r.headers["Location"]
    assert Usuario.query.filter_by(email="intruso@x.com").count() == 0


# E02 – página 405 em inglês
def test_e02_pagina_405_em_portugues(logado):
    r = logado.get("/clientes/1/excluir")
    html = r.get_data(as_text=True)
    assert r.status_code == 405 and "Use os botões do sistema" in html


# E03 – textos sem limite de tamanho
def test_e03_nome_cliente_muito_longo(app):
    with pytest.raises(ErroValidacao, match="no máximo 100"):
        Cliente().preencher("A" * 300, "61955554444")


def test_e03_nome_servico_muito_longo(app):
    with pytest.raises(ErroValidacao, match="no máximo 80"):
        Servico().preencher("B" * 81, 30, 10)


# E04 – fuso horário do servidor
def test_e04_agora_usa_fuso_do_salao_mesmo_com_servidor_em_utc():
    original = os.environ.get("TZ")
    os.environ["TZ"] = "UTC"
    time.tzset()
    try:
        esperado = datetime.now(ZoneInfo("America/Sao_Paulo")).replace(tzinfo=None)
        assert abs(agora() - esperado) < timedelta(seconds=5)
    finally:
        if original is None:
            os.environ.pop("TZ")
        else:
            os.environ["TZ"] = original
        time.tzset()


# E05 – editar atendimento cujo horário já passou
def test_e05_editar_observacao_de_horario_passado(cliente, servico):
    ini = datetime.now().replace(second=0, microsecond=0) - timedelta(hours=1)
    a = Agendamento(cliente=cliente, servico=servico, inicio=ini,
                    fim=ini + timedelta(minutes=60), status="agendado")
    db.session.add(a)
    db.session.commit()
    a.preencher(cliente, servico, ini, "cliente chegou atrasada",
                agora=ini + timedelta(hours=1))
    db.session.commit()
    assert a.observacao == "cliente chegou atrasada"


def test_e05_mudar_para_horario_passado_continua_bloqueado(cliente, servico):
    a = Agendamento(status="agendado")
    with db.session.no_autoflush:
        a.preencher(cliente, servico, proximo_dia_util(10))
    db.session.add(a)
    db.session.commit()
    with pytest.raises(ErroValidacao, match="passada"):
        a.preencher(cliente, servico, datetime.now() - timedelta(days=1))


# E06 – formatação do faturamento
def test_e06_moeda_com_separador_de_milhar():
    assert formatar_moeda(1500) == "R$ 1.500,00"


# E07 – preço no formato brasileiro
@pytest.mark.parametrize("texto,valor", [("1.234,56", 1234.56), ("80,50", 80.5), ("80", 80.0),
                                         ("R$ 35,00", 35.0), ("99.9", 99.9)])
def test_e07_preco_formato_brasileiro(app, texto, valor):
    s = Servico()
    s.preencher("Teste", 30, texto)
    assert float(s.preco) == valor


# E08 – preço acima do limite do banco
def test_e08_preco_acima_do_limite(app):
    with pytest.raises(ErroValidacao, match="máximo"):
        Servico().preencher("Luxo", 60, "99999999")
