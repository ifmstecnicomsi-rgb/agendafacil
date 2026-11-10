from . import ErroValidacao, db, formatar_moeda, validar_tamanho

PRECO_MAXIMO = 999999.99


def converter_preco(texto):
    """Aceita 80, 80.5, 80,50 e 1.234,56."""
    t = str(texto if texto is not None else "").strip().replace("R$", "").replace(" ", "")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    return float(t)


class Servico(db.Model):
    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)
    duracao_min = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(8, 2), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    agendamentos = db.relationship("Agendamento", back_populates="servico", lazy="dynamic")

    @property
    def preco_formatado(self):
        return formatar_moeda(self.preco)

    def preencher(self, nome, duracao_min, preco, ativo=True):
        nome = (nome or "").strip()
        if len(nome) < 2:
            raise ErroValidacao("Informe o nome do serviço.")
        validar_tamanho(nome, 80, "O nome")
        existente = Servico.query.filter(db.func.lower(Servico.nome) == nome.lower()).first()
        if existente and existente.id != self.id:
            raise ErroValidacao("Já existe um serviço com este nome.")
        try:
            duracao = int(duracao_min)
        except (TypeError, ValueError):
            raise ErroValidacao("Duração deve ser um número inteiro de minutos.")
        if not 5 <= duracao <= 480:
            raise ErroValidacao("Duração deve ficar entre 5 e 480 minutos.")
        try:
            valor = converter_preco(preco)
        except (TypeError, ValueError):
            raise ErroValidacao("Preço inválido.")
        if valor < 0:
            raise ErroValidacao("O preço não pode ser negativo.")
        if valor > PRECO_MAXIMO:
            raise ErroValidacao("Preço máximo permitido: R$ 999.999,99.")
        self.nome, self.duracao_min, self.preco, self.ativo = nome, duracao, round(valor, 2), bool(ativo)
