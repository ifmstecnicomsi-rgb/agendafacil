from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from ..models import Cliente, ErroValidacao, db
from . import login_obrigatorio

bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@bp.route("/")
@login_obrigatorio
def listar():
    termo = request.args.get("q", "")
    return render_template("clientes/lista.html", clientes=Cliente.buscar(termo), termo=termo)


@bp.route("/novo", methods=["GET", "POST"])
@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def formulario(id=None):
    cliente = db.session.get(Cliente, id) if id else Cliente()
    if cliente is None:
        abort(404)
    if request.method == "POST":
        try:
            cliente.preencher(request.form.get("nome"), request.form.get("telefone"),
                              request.form.get("email"))
            db.session.add(cliente)
            db.session.commit()
            flash("Cliente salvo com sucesso.", "sucesso")
            return redirect(url_for("clientes.listar"))
        except ErroValidacao as e:
            db.session.rollback()
            flash(str(e), "erro")
    return render_template("clientes/form.html", cliente=cliente, dados=request.form)


@bp.route("/<int:id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir(id):
    cliente = db.session.get(Cliente, id) or abort(404)
    if not cliente.pode_excluir():
        flash("Cliente possui agendamentos em aberto e não pode ser excluído.", "erro")
    elif cliente.agendamentos.count() > 0:
        flash("Cliente possui histórico de atendimentos e não pode ser excluído.", "erro")
    else:
        db.session.delete(cliente)
        db.session.commit()
        flash("Cliente excluído.", "sucesso")
    return redirect(url_for("clientes.listar"))
