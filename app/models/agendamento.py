from datetime import datetime, timedelta

from flask import current_app

from . import ErroValidacao, agora as agora_local, db

STATUS_VALIDOS = ("agendado", "concluido", "cancelado")


class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey("servicos.id"), nullable=False)
    inicio = db.Column(db.DateTime, nullable=False)
    fim = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False, default="agendado")
    observacao = db.Column(db.String(255), nullable=True)

    cliente = db.relationship("Cliente", back_populates="agendamentos")
    servico = db.relationship("Servico", back_populates="agendamentos")

    __table_args__ = (
        db.CheckConstraint("status IN ('agendado','concluido','cancelado')", name="ck_status"),
        db.CheckConstraint("fim > inicio", name="ck_intervalo"),
    )

    def preencher(self, cliente, servico, inicio, observacao=None, agora=None):
        """Valida as regras de negócio do agendamento."""
        agora = agora or agora_local()
        if cliente is None:
            raise ErroValidacao("Selecione um cliente.")
        if servico is None or not servico.ativo:
            raise ErroValidacao("Selecione um serviço ativo.")
        if isinstance(inicio, str):
            try:
                inicio = datetime.strptime(inicio, "%Y-%m-%dT%H:%M")
            except ValueError:
                raise ErroValidacao("Data e hora inválidas.")
        # Na edição, um horário que já passou pode ser mantido (ex.: só mudar a observação)
        mantendo_horario = self.id is not None and inicio == self.inicio
        if inicio < agora and not mantendo_horario:
            raise ErroValidacao("Não é possível agendar em data/hora passada.")

        fim = inicio + timedelta(minutes=servico.duracao_min)
        abre = current_app.config["HORA_ABERTURA"]
        fecha = current_app.config["HORA_FECHAMENTO"]
        limite = inicio.replace(hour=fecha, minute=0, second=0, microsecond=0)
        if inicio.hour < abre or fim > limite:
            raise ErroValidacao(f"Horário fora do funcionamento ({abre:02d}h às {fecha:02d}h).")
        if inicio.weekday() == 6:
            raise ErroValidacao("O salão não funciona aos domingos.")

        conflito = Agendamento.query.filter(
            Agendamento.status == "agendado",
            Agendamento.inicio < fim,
            Agendamento.fim > inicio,
            Agendamento.id != (self.id or 0),
        ).first()
        if conflito:
            raise ErroValidacao(
                f"Conflito de horário com {conflito.cliente.nome} "
                f"({conflito.inicio:%H:%M}–{conflito.fim:%H:%M})."
            )

        self.cliente, self.servico = cliente, servico
        self.inicio, self.fim = inicio, fim
        self.observacao = (observacao or "").strip()[:255] or None

    def alterar_status(self, novo_status):
        if novo_status not in STATUS_VALIDOS:
            raise ErroValidacao("Status inválido.")
        if self.status != "agendado":
            raise ErroValidacao("Só é possível alterar agendamentos em aberto.")
        self.status = novo_status

    @classmethod
    def do_dia(cls, dia=None):
        dia = dia or agora_local().date()
        ini = datetime.combine(dia, datetime.min.time())
        return cls.query.filter(cls.inicio >= ini, cls.inicio < ini + timedelta(days=1)) \
            .order_by(cls.inicio).all()
