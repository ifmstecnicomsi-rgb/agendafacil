-- AgendaFácil · Projeto físico do banco de dados (SQLite)
-- Gerado a partir dos Models (SQLAlchemy)

CREATE TABLE clientes (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	telefone VARCHAR(11) NOT NULL, 
	email VARCHAR(120), 
	criado_em DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (telefone)
);

CREATE TABLE servicos (
	id INTEGER NOT NULL, 
	nome VARCHAR(80) NOT NULL, 
	duracao_min INTEGER NOT NULL, 
	preco NUMERIC(8, 2) NOT NULL, 
	ativo BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
);

CREATE TABLE usuarios (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	senha_hash VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);

CREATE TABLE agendamentos (
	id INTEGER NOT NULL, 
	cliente_id INTEGER NOT NULL, 
	servico_id INTEGER NOT NULL, 
	inicio DATETIME NOT NULL, 
	fim DATETIME NOT NULL, 
	status VARCHAR(10) NOT NULL, 
	observacao VARCHAR(255), 
	PRIMARY KEY (id), 
	CONSTRAINT ck_status CHECK (status IN ('agendado','concluido','cancelado')), 
	CONSTRAINT ck_intervalo CHECK (fim > inicio), 
	FOREIGN KEY(cliente_id) REFERENCES clientes (id), 
	FOREIGN KEY(servico_id) REFERENCES servicos (id)
);

