
from flask import Blueprint, render_template

from ..models import Agendamento, Cliente, Servico, agora, formatar_moeda
from . import login_obrigatorio

bp = Blueprint("painel", __name__)


@bp.route("/")
@login_obrigatorio
def inicio():
    hoje = Agendamento.do_dia(agora().date())
    proximos = Agendamento.query.filter(
        Agendamento.status == "agendado", Agendamento.inicio >= agora()
    ).order_by(Agendamento.inicio).limit(5).all()
    faturamento = sum(float(a.servico.preco) for a in hoje if a.status == "concluido")
    return render_template(
        "painel.html",
        hoje=hoje,
        proximos=proximos,
        total_clientes=Cliente.query.count(),
        total_servicos=Servico.query.filter_by(ativo=True).count(),
        faturamento=formatar_moeda(faturamento),
    )
