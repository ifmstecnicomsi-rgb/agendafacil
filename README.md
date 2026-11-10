# ✂ AgendaFácil

Sistema web de **agendamento para salões de beleza**, desenvolvido no **Projeto Integrador Transdisciplinar em Engenharia de Software II**.

O AgendaFácil substitui a agenda de papel e o WhatsApp como controle de horários: cadastra clientes e serviços, marca atendimentos **sem conflito de horário**, respeita o horário de funcionamento e mostra no painel o movimento do dia.

> **Uso de IA:** o código-fonte e a documentação deste projeto foram desenvolvidos com a ferramenta de inteligência artificial **Claude (Anthropic)**. Os 5 testes com usuários são simulações fictícias geradas por IA. Ver a [declaração](docs/situacao-3-testes/declaracao-uso-de-ia.md).

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Back-end | Python 3 + Flask (padrão **MVC**) |
| ORM / Banco de dados | SQLAlchemy + **SQLite** |
| Front-end | HTML5, CSS3 e JavaScript puro (templates Jinja2) |
| Testes | pytest (54 testes unitários, de integração e de regressão) |
| Hospedagem | PythonAnywhere (plano gratuito) |
| Versionamento | Git + GitHub |

## Funcionalidades

- Login e logout; novos usuários são cadastrados por quem já está logado (senhas com *hash*)
- Cadastro, edição, busca e exclusão de **clientes** (telefone com máscara e validação)
- Cadastro, edição, desativação e exclusão de **serviços** (duração e preço)
- **Agendamentos** com cálculo automático do término e bloqueio de:
  - horário já ocupado (conflito)
  - data/hora no passado
  - fora do expediente (08h–20h) e domingos
- Concluir ou cancelar atendimento (cancelado libera o horário)
- Agenda por dia e painel com indicadores (atendimentos do dia, clientes, serviços e faturamento)
- Datas e horários sempre no fuso de Brasília, mesmo com o servidor em outro fuso
- Páginas de erro amigáveis (400, 404, 405, 500), proteção CSRF e layout responsivo (celular)

## Estrutura do repositório

```
agendafacil/
├── app/
│   ├── models/          # MODEL: entidades e regras de negócio
│   ├── controllers/     # CONTROLLER: rotas (Blueprints)
│   ├── views/           # VIEW: templates HTML (Jinja2)
│   ├── static/          # CSS e JavaScript
│   ├── config.py
│   └── __init__.py      # fábrica da aplicação e tratamento de erros
├── database/schema.sql  # projeto físico do banco
├── tests/               # testes automatizados (pytest)
├── docs/
│   ├── situacao-1-planejamento/   # escopo, UML, banco de dados, IHC
│   ├── situacao-2-codificacao/    # arquitetura, manual de uso, publicação, telas
│   ├── situacao-3-testes/         # testes, formulário dos colegas, laudo de qualidade
│   └── videos/                    # roteiros dos vídeos
├── run.py
└── requirements.txt
```

## Como executar localmente

```bash
git clone https://github.com/SEU-USUARIO/agendafacil.git
cd agendafacil
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Acesse **http://127.0.0.1:5000** e entre com o usuário padrão:

- **E-mail:** admin@agendafacil.com
- **Senha:** admin123

(Pode ser alterado pelas variáveis de ambiente `ADMIN_EMAIL` e `ADMIN_SENHA`. O fuso horário padrão é `America/Sao_Paulo` e pode ser trocado pela variável `APP_TZ`.)

## Como rodar os testes

```bash
python -m pytest -v
```

Resultado atual (versão 1.1): **54 testes aprovados**. Detalhes em [`docs/situacao-3-testes/testes-automatizados.md`](docs/situacao-3-testes/testes-automatizados.md).

## Documentação

| Situação | Documento |
|---|---|
| 1 – Planejamento | [Escopo e requisitos](docs/situacao-1-planejamento/01-escopo-e-requisitos.md) · [Modelagem UML](docs/situacao-1-planejamento/02-modelagem-uml.md) · [Banco de dados e dicionário](docs/situacao-1-planejamento/03-banco-de-dados.md) · [IHC e protótipo](docs/situacao-1-planejamento/04-ihc-prototipo.md) |
| 2 – Codificação | [Arquitetura MVC](docs/situacao-2-codificacao/arquitetura-mvc.md) · [Manual de uso](docs/situacao-2-codificacao/manual-de-uso.md) · [Publicação](docs/situacao-2-codificacao/publicacao-pythonanywhere.md) |
| 3 – Testes | [Testes automatizados](docs/situacao-3-testes/testes-automatizados.md) · [Roteiro para os colegas](docs/situacao-3-testes/roteiro-de-teste-colegas.md) · [Formulário de teste](docs/situacao-3-testes/formulario-de-teste.md) · [Laudo de qualidade](docs/situacao-3-testes/laudo-de-qualidade.md) |
| Vídeos | [Roteiros](docs/videos/roteiros.md) |

## Histórico de versões

| Versão | Mudanças |
|---|---|
| 1.0 | Primeira versão funcional. |
| 1.1 | Correção de 8 erros encontrados nos testes exploratórios: cadastro aberto a visitantes, fuso horário, limite de textos, edição de horário passado, página 405, formatação de moeda, preço em formato brasileiro e limite de preço. Ver o [Laudo de Qualidade](docs/situacao-3-testes/laudo-de-qualidade.md). |

## Links

- **Sistema em funcionamento:** https://SEU-USUARIO.pythonanywhere.com
- **Vídeo de apresentação:** _inserir link_
- **Vídeo das correções:** _inserir link_
