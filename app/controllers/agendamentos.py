from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from ..models import Agendamento, Cliente, ErroValidacao, Servico, agora, db
from . import login_obrigatorio

bp = Blueprint("agendamentos", __name__, url_prefix="/agendamentos")


@bp.route("/")
@login_obrigatorio
def listar():
    texto = request.args.get("data")
    try:
        dia = datetime.strptime(texto, "%Y-%m-%d").date() if texto else agora().date()
    except ValueError:
        flash("Data inválida; exibindo hoje.", "aviso")
        dia = agora().date()
    return render_template("agendamentos/lista.html", agendamentos=Agendamento.do_dia(dia), dia=dia)


@bp.route("/novo", methods=["GET", "POST"])
@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def formulario(id=None):
    ag = db.session.get(Agendamento, id) if id else Agendamento(status="agendado")
    if ag is None:
        abort(404)
    if id and ag.status != "agendado":
        flash("Agendamentos concluídos ou cancelados não podem ser editados.", "erro")
        return redirect(url_for("agendamentos.listar"))
    if request.method == "POST":
        try:
            cliente = db.session.get(Cliente, request.form.get("cliente_id", type=int) or 0)
            servico = db.session.get(Servico, request.form.get("servico_id", type=int) or 0)
            with db.session.no_autoflush:
                ag.preencher(cliente, servico, request.form.get("inicio"),
                             request.form.get("observacao"))
            db.session.add(ag)
            db.session.commit()
            flash("Agendamento salvo com sucesso.", "sucesso")
            return redirect(url_for("agendamentos.listar", data=ag.inicio.date().isoformat()))
        except ErroValidacao as e:
            db.session.rollback()
            flash(str(e), "erro")
    return render_template(
        "agendamentos/form.html", ag=ag, dados=request.form,
        clientes=Cliente.query.order_by(Cliente.nome).all(),
        servicos=Servico.query.filter_by(ativo=True).order_by(Servico.nome).all(),
    )


@bp.route("/<int:id>/status/<novo>", methods=["POST"])
@login_obrigatorio
def status(id, novo):
    ag = db.session.get(Agendamento, id) or abort(404)
    try:
        ag.alterar_status(novo)
        db.session.commit()
        flash("Status atualizado.", "sucesso")
    except ErroValidacao as e:
        flash(str(e), "erro")
    return redirect(url_for("agendamentos.listar", data=ag.inicio.date().isoformat()))
