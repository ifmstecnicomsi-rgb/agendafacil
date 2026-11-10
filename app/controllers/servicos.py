from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from ..models import ErroValidacao, Servico, db
from . import login_obrigatorio

bp = Blueprint("servicos", __name__, url_prefix="/servicos")


@bp.route("/")
@login_obrigatorio
def listar():
    return render_template("servicos/lista.html", servicos=Servico.query.order_by(Servico.nome).all())


@bp.route("/novo", methods=["GET", "POST"])
@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def formulario(id=None):
    servico = db.session.get(Servico, id) if id else Servico(ativo=True)
    if servico is None:
        abort(404)
    if request.method == "POST":
        try:
            servico.preencher(request.form.get("nome"), request.form.get("duracao_min"),
                              request.form.get("preco"), request.form.get("ativo") == "on")
            db.session.add(servico)
            db.session.commit()
            flash("Serviço salvo com sucesso.", "sucesso")
            return redirect(url_for("servicos.listar"))
        except ErroValidacao as e:
            db.session.rollback()
            flash(str(e), "erro")
    return render_template("servicos/form.html", servico=servico, dados=request.form)


@bp.route("/<int:id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir(id):
    servico = db.session.get(Servico, id) or abort(404)
    if servico.agendamentos.count() > 0:
        servico.ativo = False
        db.session.commit()
        flash("Serviço possui agendamentos; foi apenas desativado.", "aviso")
    else:
        db.session.delete(servico)
        db.session.commit()
        flash("Serviço excluído.", "sucesso")
    return redirect(url_for("servicos.listar"))
