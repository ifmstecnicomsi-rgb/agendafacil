"""Testes de integração: Controllers + Views + banco."""
from app.models import Agendamento, Cliente, Servico
from conftest import proximo_dia_util


def test_redireciona_para_login_sem_sessao(client):
    r = client.get("/")
    assert r.status_code == 302 and "/login" in r.headers["Location"]


def test_login_invalido(client):
    r = client.post("/login", data={"email": "admin@agendafacil.com", "senha": "x"})
    assert "E-mail ou senha incorretos" in r.get_data(as_text=True)


def test_login_valido_abre_painel(logado):
    r = logado.get("/")
    assert r.status_code == 200 and "Painel" in r.get_data(as_text=True)


def test_cadastro_de_usuario(logado):
    r = logado.post("/cadastro", data={"nome": "Carla Dias", "email": "carla@email.com",
                                       "senha": "segredo1", "confirmar": "segredo1"},
                    follow_redirects=True)
    assert "Usuário Carla Dias cadastrado" in r.get_data(as_text=True)


def test_cadastro_senhas_diferentes(logado):
    r = logado.post("/cadastro", data={"nome": "Carla", "email": "c@email.com",
                                       "senha": "segredo1", "confirmar": "outra123"})
    assert "não conferem" in r.get_data(as_text=True)


def test_crud_cliente(logado):
    r = logado.post("/clientes/novo", data={"nome": "José Silva", "telefone": "(61) 98888-7777"},
                    follow_redirects=True)
    assert "Cliente salvo" in r.get_data(as_text=True)
    c = Cliente.query.one()
    r = logado.post(f"/clientes/{c.id}/editar",
                    data={"nome": "José da Silva", "telefone": "61988887777"}, follow_redirects=True)
    assert "José da Silva" in r.get_data(as_text=True)
    r = logado.post(f"/clientes/{c.id}/excluir", follow_redirects=True)
    assert "Cliente excluído" in r.get_data(as_text=True)
    assert Cliente.query.count() == 0


def test_cliente_invalido_mostra_erro_e_mantem_dados(logado):
    r = logado.post("/clientes/novo", data={"nome": "José", "telefone": "123"})
    html = r.get_data(as_text=True)
    assert "Telefone inválido" in html and 'value="José"' in html


def test_cliente_inexistente_404(logado):
    assert logado.get("/clientes/999/editar").status_code == 404


def test_crud_servico(logado):
    r = logado.post("/servicos/novo", data={"nome": "Manicure", "duracao_min": "40",
                                            "preco": "35.00", "ativo": "on"}, follow_redirects=True)
    assert "Manicure" in r.get_data(as_text=True)
    assert Servico.query.one().ativo is True


def test_fluxo_completo_de_agendamento(logado, cliente, servico):
    inicio = proximo_dia_util(14).strftime("%Y-%m-%dT%H:%M")
    r = logado.post("/agendamentos/novo", data={"cliente_id": cliente.id, "servico_id": servico.id,
                                                "inicio": inicio}, follow_redirects=True)
    assert "Agendamento salvo" in r.get_data(as_text=True)
    ag = Agendamento.query.one()

    # conflito pela interface
    r = logado.post("/agendamentos/novo", data={"cliente_id": cliente.id, "servico_id": servico.id,
                                                "inicio": inicio})
    assert "Conflito de horário" in r.get_data(as_text=True)

    # concluir
    logado.post(f"/agendamentos/{ag.id}/status/concluido")
    assert Agendamento.query.one().status == "concluido"

    # não pode editar concluído
    r = logado.get(f"/agendamentos/{ag.id}/editar", follow_redirects=True)
    assert "não podem ser editados" in r.get_data(as_text=True)


def test_cliente_com_agendamento_nao_exclui(logado, cliente, servico):
    logado.post("/agendamentos/novo", data={"cliente_id": cliente.id, "servico_id": servico.id,
                                            "inicio": proximo_dia_util(9).strftime("%Y-%m-%dT%H:%M")})
    r = logado.post(f"/clientes/{cliente.id}/excluir", follow_redirects=True)
    assert "não pode ser excluído" in r.get_data(as_text=True)


def test_agenda_data_invalida(logado):
    r = logado.get("/agendamentos/?data=abc")
    assert "Data inválida" in r.get_data(as_text=True)


def test_logout(logado):
    logado.get("/logout")
    assert logado.get("/").status_code == 302
