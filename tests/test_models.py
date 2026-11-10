"""Testes unitários da camada Model (regras de negócio)."""
from datetime import datetime, timedelta

import pytest

from app.models import Agendamento, Cliente, ErroValidacao, Servico, Usuario, db
from conftest import proximo_dia_util


# ---------- Usuário ----------
def test_cadastrar_usuario_e_autenticar(app):
    Usuario.cadastrar("Ana Lima", "ANA@email.com", "segredo1")
    assert Usuario.autenticar("ana@email.com", "segredo1") is not None
    assert Usuario.autenticar("ana@email.com", "errada") is None


def test_senha_curta_rejeitada(app):
    with pytest.raises(ErroValidacao, match="6 caracteres"):
        Usuario.cadastrar("Ana", "ana@email.com", "123")


def test_email_duplicado_rejeitado(app):
    with pytest.raises(ErroValidacao, match="Já existe"):
        Usuario.cadastrar("Outro", "admin@agendafacil.com", "segredo1")


def test_senha_armazenada_com_hash(app):
    u = Usuario.cadastrar("Bia", "bia@email.com", "segredo1")
    assert u.senha_hash != "segredo1"


# ---------- Cliente ----------
def test_telefone_normalizado_e_formatado(cliente):
    assert cliente.telefone == "61999991234"
    assert cliente.telefone_formatado == "(61) 99999-1234"


@pytest.mark.parametrize("tel", ["123", "6199999", "(61) 99999-12345", ""])
def test_telefone_invalido(app, tel):
    with pytest.raises(ErroValidacao, match="Telefone"):
        Cliente().preencher("João", tel)


def test_telefone_duplicado(cliente):
    with pytest.raises(ErroValidacao, match="telefone"):
        Cliente().preencher("Outra Maria", "61999991234")


def test_email_cliente_invalido(app):
    with pytest.raises(ErroValidacao, match="E-mail"):
        Cliente().preencher("João", "61988887777", "joao@")


def test_busca_cliente_por_nome(cliente):
    assert Cliente.buscar("maria") == [cliente]
    assert Cliente.buscar("inexistente") == []


# ---------- Serviço ----------
def test_servico_preco_formatado(servico):
    assert servico.preco_formatado == "R$ 80,00"


@pytest.mark.parametrize("duracao", [0, 1000, "abc"])
def test_servico_duracao_invalida(app, duracao):
    with pytest.raises(ErroValidacao, match="Duração"):
        Servico().preencher("Escova", duracao, 50)


def test_servico_preco_negativo(app):
    with pytest.raises(ErroValidacao, match="negativo"):
        Servico().preencher("Escova", 30, -10)


# ---------- Agendamento ----------
def _agendar(cliente, servico, inicio):
    a = Agendamento(status="agendado")
    with db.session.no_autoflush:
        a.preencher(cliente, servico, inicio)
    db.session.add(a)
    db.session.commit()
    return a


def test_agendamento_calcula_fim(cliente, servico):
    inicio = proximo_dia_util(10)
    a = _agendar(cliente, servico, inicio)
    assert a.fim == inicio + timedelta(minutes=60)


def test_agendamento_no_passado(cliente, servico):
    with pytest.raises(ErroValidacao, match="passada"):
        Agendamento().preencher(cliente, servico, datetime.now() - timedelta(hours=1))


def test_agendamento_fora_do_horario(cliente, servico):
    with pytest.raises(ErroValidacao, match="funcionamento"):
        Agendamento().preencher(cliente, servico, proximo_dia_util(7))
    with pytest.raises(ErroValidacao, match="funcionamento"):
        Agendamento().preencher(cliente, servico, proximo_dia_util(19, 30))  # terminaria 20:30


def test_agendamento_no_domingo(cliente, servico):
    d = datetime.now() + timedelta(days=1)
    while d.weekday() != 6:
        d += timedelta(days=1)
    with pytest.raises(ErroValidacao, match="domingos"):
        Agendamento().preencher(cliente, servico, d.replace(hour=10, minute=0))


def test_conflito_de_horario(cliente, servico):
    _agendar(cliente, servico, proximo_dia_util(10))
    with pytest.raises(ErroValidacao, match="Conflito"):
        Agendamento().preencher(cliente, servico, proximo_dia_util(10, 30))


def test_horario_encostado_nao_conflita(cliente, servico):
    _agendar(cliente, servico, proximo_dia_util(10))
    a = _agendar(cliente, servico, proximo_dia_util(11))  # começa quando o outro termina
    assert a.id is not None


def test_cancelado_libera_horario(cliente, servico):
    a = _agendar(cliente, servico, proximo_dia_util(10))
    a.alterar_status("cancelado")
    db.session.commit()
    b = _agendar(cliente, servico, proximo_dia_util(10))
    assert b.id is not None


def test_nao_altera_status_finalizado(cliente, servico):
    a = _agendar(cliente, servico, proximo_dia_util(10))
    a.alterar_status("concluido")
    with pytest.raises(ErroValidacao, match="em aberto"):
        a.alterar_status("cancelado")


def test_servico_inativo_nao_agenda(cliente, servico):
    servico.ativo = False
    with pytest.raises(ErroValidacao, match="ativo"):
        Agendamento().preencher(cliente, servico, proximo_dia_util(10))


def test_data_texto_invalida(cliente, servico):
    with pytest.raises(ErroValidacao, match="inválidas"):
        Agendamento().preencher(cliente, servico, "31/02/2025 10h")
