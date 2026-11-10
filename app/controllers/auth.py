from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from ..models import ErroValidacao
from ..models.usuario import Usuario
from . import login_obrigatorio

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = Usuario.autenticar(request.form.get("email"), request.form.get("senha"))
        if usuario:
            csrf = session.get("_csrf")
            session.clear()
            if csrf:
                session["_csrf"] = csrf
            session["usuario_id"] = usuario.id
            flash(f"Bem-vindo(a), {usuario.nome}!", "sucesso")
            return redirect(url_for("painel.inicio"))
        flash("E-mail ou senha incorretos.", "erro")
    return render_template("auth/login.html")


@bp.route("/cadastro", methods=["GET", "POST"])
@login_obrigatorio
def cadastro():
    """Somente um usuário já logado pode cadastrar outro (equipe do salão)."""
    if request.method == "POST":
        try:
            if request.form.get("senha") != request.form.get("confirmar"):
                raise ErroValidacao("As senhas não conferem.")
            novo = Usuario.cadastrar(request.form.get("nome"), request.form.get("email"),
                                     request.form.get("senha"))
            flash(f"Usuário {novo.nome} cadastrado. Ele já pode entrar com o e-mail e a senha informados.", "sucesso")
            return redirect(url_for("painel.inicio"))
        except ErroValidacao as e:
            flash(str(e), "erro")
    return render_template("auth/cadastro.html")


@bp.route("/logout")
def logout():
    session.pop("usuario_id", None)
    flash("Você saiu do sistema.", "sucesso")
    return redirect(url_for("auth.login"))
