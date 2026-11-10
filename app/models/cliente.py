import re

from . import ErroValidacao, agora, db, validar_tamanho

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalizar_telefone(telefone):
    """Mantém só os dígitos e exige 10 ou 11 dígitos (DDD + número)."""
    digitos = re.sub(r"\D", "", telefone or "")
    if len(digitos) not in (10, 11):
        raise ErroValidacao("Telefone inválido. Use DDD + número, ex.: (61) 99999-9999.")
    return digitos


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=agora)

    agendamentos = db.relationship("Agendamento", back_populates="cliente", lazy="dynamic")

    @property
    def telefone_formatado(self):
        t = self.telefone
        if len(t) == 11:
            return f"({t[:2]}) {t[2:7]}-{t[7:]}"
        return f"({t[:2]}) {t[2:6]}-{t[6:]}"

    def preencher(self, nome, telefone, email=None):
        nome = (nome or "").strip()
        email = (email or "").strip().lower() or None
        if len(nome) < 2:
            raise ErroValidacao("Informe o nome do cliente.")
        validar_tamanho(nome, 100, "O nome")
        tel = normalizar_telefone(telefone)
        existente = Cliente.query.filter_by(telefone=tel).first()
        if existente and existente.id != self.id:
            raise ErroValidacao("Já existe um cliente com este telefone.")
        if email:
            validar_tamanho(email, 120, "O e-mail")
        if email and not EMAIL_RE.match(email):
            raise ErroValidacao("E-mail inválido.")
        self.nome, self.telefone, self.email = nome, tel, email

    def pode_excluir(self):
        return self.agendamentos.filter_by(status="agendado").count() == 0

    @classmethod
    def buscar(cls, termo=None):
        q = cls.query
        if termo:
            like = f"%{termo.strip()}%"
            q = q.filter(db.or_(cls.nome.ilike(like), cls.telefone.like(like)))
        return q.order_by(cls.nome).all()
