"""Fábrica da aplicação AgendaFácil (padrão MVC com Flask)."""
import secrets

from flask import Flask, abort, render_template, request, session

from .config import Config
from .models import db


def create_app(config_object=Config):
    app = Flask(__name__, template_folder="views", static_folder="static")
    app.config.from_object(config_object)

    db.init_app(app)

    # Controllers (Blueprints)
    from .controllers.auth import bp as auth_bp
    from .controllers.painel import bp as painel_bp
    from .controllers.clientes import bp as clientes_bp
    from .controllers.servicos import bp as servicos_bp
    from .controllers.agendamentos import bp as agendamentos_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(painel_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(servicos_bp)
    app.register_blueprint(agendamentos_bp)

    # Proteção CSRF simples: todo formulário POST carrega um token da sessão
    def gerar_csrf():
        if "_csrf" not in session:
            session["_csrf"] = secrets.token_hex(16)
        return session["_csrf"]

    app.jinja_env.globals["csrf_token"] = gerar_csrf

    @app.before_request
    def validar_csrf():
        if app.config.get("CSRF_ENABLED", True) and request.method == "POST":
            token = request.form.get("_csrf")
            if not token or token != session.get("_csrf"):
                abort(400)

    # Tratamento de erros com páginas amigáveis
    @app.errorhandler(400)
    def erro_400(e):
        return render_template("erros/erro.html", codigo=400,
                               mensagem="Requisição inválida. Recarregue a página e tente novamente."), 400

    @app.errorhandler(404)
    def erro_404(e):
        return render_template("erros/erro.html", codigo=404,
                               mensagem="Página não encontrada."), 404

    @app.errorhandler(405)
    def erro_405(e):
        return render_template("erros/erro.html", codigo=405,
                               mensagem="Esta ação não pode ser feita por este caminho. Use os botões do sistema."), 405

    @app.errorhandler(500)
    def erro_500(e):
        db.session.rollback()
        return render_template("erros/erro.html", codigo=500,
                               mensagem="Ocorreu um erro interno. Tente novamente em instantes."), 500

    with app.app_context():
        db.create_all()
        from .models.usuario import Usuario
        Usuario.criar_admin_padrao(app.config["ADMIN_EMAIL"], app.config["ADMIN_SENHA"])

    return app
