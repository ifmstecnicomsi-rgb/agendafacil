"""Camada Controller: recebe as requisições, aciona os Models e escolhe a View."""
from functools import wraps

from flask import g, redirect, session, url_for

from ..models import db
from ..models.usuario import Usuario


def login_obrigatorio(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        uid = session.get("usuario_id")
        g.usuario = db.session.get(Usuario, uid) if uid else None
        if g.usuario is None:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapper
