import re

from werkzeug.security import check_password_hash, generate_password_hash

from . import ErroValidacao, db, validar_tamanho

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

    def definir_senha(self, senha):
        if not senha or len(senha) < 6:
            raise ErroValidacao("A senha deve ter pelo menos 6 caracteres.")
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha or "")

    @classmethod
    def cadastrar(cls, nome, email, senha):
        nome = (nome or "").strip()
        email = (email or "").strip().lower()
        if len(nome) < 2:
            raise ErroValidacao("Informe o nome completo.")
        validar_tamanho(nome, 100, "O nome")
        validar_tamanho(email, 120, "O e-mail")
        if not EMAIL_RE.match(email):
            raise ErroValidacao("E-mail inválido.")
        if cls.query.filter_by(email=email).first():
            raise ErroValidacao("Já existe um usuário com este e-mail.")
        usuario = cls(nome=nome, email=email)
        usuario.definir_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @classmethod
    def autenticar(cls, email, senha):
        usuario = cls.query.filter_by(email=(email or "").strip().lower()).first()
        if usuario and usuario.verificar_senha(senha):
            return usuario
        return None

    @classmethod
    def criar_admin_padrao(cls, email, senha):
        if not cls.query.filter_by(email=email).first():
            usuario = cls(nome="Administrador", email=email)
            usuario.definir_senha(senha)
            db.session.add(usuario)
            db.session.commit()
