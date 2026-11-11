# Laudo de Qualidade – AgendaFácil

## 1. Identificação

| Item | Informação |
|---|---|
| Sistema | AgendaFácil – agendamento para salões de beleza |
| Versão testada | 1.0 |
| Versão corrigida | 1.1 |
| Endereço | https://www.ifmstecnicomsi.pythonanywhere.com |
| Responsável | _Arlan_ |

## 2. Verificação interna – testes automatizados

- **Versão 1.0:** 40 testes (pytest), 40 aprovados.
- **Versão 1.1:** 54 testes, 54 aprovados. Os 14 testes novos (`tests/test_correcoes_v11.py`) reproduzem cada erro da seção 3 e garantem que ele não volte (testes de regressão).

Detalhes em [testes-automatizados.md](testes-automatizados.md).

## 3. Testes exploratórios (versão 1.0)

**Objetivo:** tentar "quebrar" o sistema antes de entregar aos colegas, usando-o como um usuário comum e também como alguém mal-intencionado.

**Como foi feito:** o sistema foi executado em dois ambientes: no fuso de Brasília e num servidor configurado em **UTC**, que é o fuso usado pelo servidor do PythonAnywhere. Os testes foram feitos no navegador (Chromium) e por requisições diretas ao servidor. Foram 13 cenários: **8 revelaram erros** e 5 passaram sem problemas.

### 3.1 Erros encontrados e correções

| ID | O que foi testado | O que aconteceu (erro) | Gravidade | Correção na versão 1.1 | Evidência |
|---|---|---|---|---|---|
| E01 | Abrir a página de cadastro **sem estar logado** | Qualquer pessoa da internet conseguia criar uma conta e, ao entrar, via todos os clientes e telefones do salão. | **Alta** (segurança e privacidade) | O cadastro de usuários passou a exigir login: só alguém da equipe cadastra outra pessoa, pelo menu "+ Usuário". O link "Cadastre-se" saiu da tela de login. | `E01_cadastro_publico_antes.png` → `_depois.png` |
| E04 | Agendar para **hoje, daqui a 1 hora**, com o servidor em UTC | O sistema recusou com a mensagem "Não é possível agendar em data/hora passada". O servidor achava que já eram 3 horas mais tarde. A agenda de "hoje" e o painel também virariam o dia às 21h. | **Alta** (impediria o uso real depois de publicado) | Foi criada a função `agora()`, que sempre usa o fuso **America/Sao_Paulo**, independente do servidor. Todo o sistema passou a usá-la. | `E04_fuso_horario_antes.png` → `_depois.png` |
| E03 | Cadastrar cliente com **nome de 300 letras** (removendo o limite do campo pelo navegador) | O servidor aceitou e o nome estourou a tabela para fora da tela. | Média | Limite de tamanho validado também no servidor (nome 100, serviço 80, e-mail 120 caracteres). Textos longos passam a quebrar linha nas tabelas. | `E03_nome_sem_limite_antes.png` → `_depois.png` |
| E05 | **Editar só a observação** de um atendimento cujo horário já tinha passado (cliente atrasada) | O sistema bloqueou com "data/hora passada", mesmo sem mudar o horário. | Média | Na edição, manter o mesmo horário é permitido. Mudar para um horário passado continua bloqueado. | Testes `test_e05_*` |
| E02 | Acessar pelo endereço uma ação que só funciona por botão (`/clientes/1/excluir`) | Apareceu uma página técnica, em inglês ("Method Not Allowed"). | Baixa | Criada a página de erro 405 em português, no mesmo visual das outras. | `E02_pagina_405_antes.png` → `_depois.png` |
| E06 | Concluir atendimento de **R$ 1.500,00** e olhar o painel | O faturamento aparecia como "R$ 1500,00", sem o ponto de milhar e diferente do resto do sistema. | Baixa | Criada uma única função de formatação de moeda, usada em todo o sistema. | Teste `test_e06_*` |
| E07 | Enviar preço no formato brasileiro **"1.234,56"** | Mensagem "Preço inválido". | Baixa | O sistema passou a aceitar 80, 80,50, 1.234,56 e "R$ 35,00". | Teste `test_e07_*` (5 variações) |
| E08 | Cadastrar serviço com preço de **R$ 99.999.999** | O sistema aceitou um valor maior do que o banco foi projetado para guardar (NUMERIC 8,2). | Baixa | Preço limitado a R$ 999.999,99, no servidor e no formulário. | Teste `test_e08_*` |

### 3.2 Cenários que passaram sem erro

| Cenário | Resultado |
|---|---|
| Sair do sistema e apertar "voltar" no navegador | Volta para o login; os dados não aparecem. (`OK_voltar_apos_logout.png`) |
| Cadastrar cliente com nome `<script>alert(1)</script>` (ataque XSS) | O texto é exibido como texto; nenhum código foi executado. |
| Enviar um status inexistente para um agendamento | Mensagem "Status inválido". |
| Enviar cliente inválido no agendamento | Mensagem "Selecione um cliente". |
| Abrir a agenda com data absurda (ano 0001) | A página abre normalmente, sem erro interno. |

### 3.3 Erros de layout corrigidos durante o desenvolvimento

| ID | Problema | Correção |
|---|---|---|
| D01 | Nas listas, a coluna de botões (Editar/Concluir/Cancelar) ficava desalinhada e a linha da tabela aparecia quebrada. | Botões agrupados num bloco próprio dentro da célula. |
| D02 | No celular, o botão "Ver dia" quebrava em duas linhas. | Botões configurados para não quebrar o texto. |

## 4. Testes com usuários (simulados)

> **Atenção:** os 5 registros abaixo são **simulações fictícias geradas por IA** (Claude, Anthropic). Eles não foram feitos por pessoas reais. Ver [declaracao-uso-de-ia.md](declaracao-uso-de-ia.md). Os problemas relatados correspondem a erros que de fato existiam na versão 1.0 (seção 3).

| # | Testador(a) | Data | O que funcionou | O que não funcionou | Não testado | Erros |
|---|---|---|---|---|---|---|
| 1 | Simulado(a) 1 – fictício | 06/11/2026 | Login, cadastro de serviços e clientes, máscara de telefone, agendamento e bloqueio de conflito | Página de cadastro aberta sem login dava acesso aos clientes do salão | Versão no celular | E01 |
| 2 | Simulado(a) 2 – fictício | 06/11/2026 | Agenda por dia, concluir/cancelar, horário liberado após cancelar, painel | Horário de hoje recusado como "passado" no servidor (fuso) | Cadastro de usuários | E04 |
| 3 | Simulado(a) 3 – fictício | 06/11/2026 | Celular: menu ☰, tabelas em cartões, busca, mensagens nos campos | "Ver dia" quebrando linha no celular; nome muito longo estourando a tabela | Exclusão de serviço | D02, E03 |
| 4 | Simulado(a) 4 – fictício | 06/11/2026 | Cadastro e edição de serviços, desativação de serviço com histórico, bloqueio de duração inválida | Preço "1.234,56" recusado; faturamento sem ponto de milhar; preço de R$ 99.999.999 aceito | Edição de agendamento | E07, E06, E08 |
| 5 | Simulado(a) 5 – fictício | 06/11/2026 | Edição de agendamento, bloqueio de exclusão de cliente com histórico, bloqueio de domingo, logout | Não alterava a observação de atendimento atrasado; página de erro em inglês; botões desalinhados | Agendamento fora do expediente | E05, E02, D01 |

Todos os problemas foram corrigidos na versão 1.1.

## 5. Conclusão

Os testes exploratórios da versão 1.0 encontraram **8 erros**: 2 graves (cadastro aberto a qualquer pessoa e fuso horário do servidor), 2 médios e 4 leves. **Todos foram corrigidos na versão 1.1**, e cada correção ganhou um teste automatizado para o erro não voltar. A versão 1.1 é a que segue para o teste dos colegas.

Somando os testes de usuário simulados, foram 10 problemas registrados (8 de funcionamento e 2 de layout), todos corrigidos.
