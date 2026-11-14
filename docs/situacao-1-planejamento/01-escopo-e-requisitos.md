# 1. Escopo e Requisitos (revisão Kaizen)

## 1.1 Problema

Pequenos salões de beleza controlam horários em agenda de papel ou conversas de WhatsApp. Isso gera **horários marcados em duplicidade**, esquecimento de clientes, dificuldade de saber o movimento do dia e nenhum histórico de atendimentos.

## 1.2 Objetivo

Oferecer um sistema web simples, acessível pelo computador ou celular, para o salão cadastrar clientes e serviços e organizar a agenda **sem conflitos de horário**.

## 1.3 Público-alvo e atores

| Ator | Descrição |
|---|---|
| **Atendente / Proprietário(a)** | Usuário do sistema. Cadastra clientes e serviços, marca, conclui e cancela atendimentos. |
| **Cliente do salão** | Não acessa o sistema; é a pessoa atendida (dados cadastrados pelo atendente). |

## 1.4 Escopo

**Dentro do escopo (versão 1.0):** autenticação de usuários; CRUD de clientes, serviços e agendamentos; controle de status do atendimento; agenda diária; painel com indicadores.

**Fora do escopo (versões futuras):** agendamento feito pelo próprio cliente pela internet; envio de lembrete por WhatsApp/SMS; controle de profissionais (vários atendimentos simultâneos); controle financeiro completo e estoque.

## 1.5 Decisões da revisão do planejamento (Kaizen)

| # | Decisão | Motivo |
|---|---|---|
| 1 | Escopo reduzido para **um profissional por horário** | Garantir entrega funcional e testada no prazo; múltiplos profissionais ficam para a v2. |
| 2 | Inclusão da regra de **horário de funcionamento** (seg–sáb, 08h–20h) | Evitar agendamentos impossíveis, apontado na revisão. |
| 3 | **Serviço com duração** em minutos e cálculo automático do fim | Necessário para detectar conflito de horário corretamente. |
| 4 | Serviço com agendamentos é **desativado** em vez de excluído | Preservar o histórico (integridade referencial). |
| 5 | Inclusão de **status** (agendado/concluído/cancelado) | Permitir histórico e liberar horário quando cancelado. |
| 6 | Definição de SGBD **SQLite** via SQLAlchemy | Banco popular, sem servidor, fácil de manter; a troca para PostgreSQL/MySQL exige apenas mudar a variável `DATABASE_URL`. |

## 1.6 Requisitos funcionais

| ID | Requisito |
|---|---|
| RF01 | O sistema deve permitir login e logout de usuários cadastrados. |
| RF02 | O sistema deve permitir que um usuário logado cadastre novos usuários da equipe (nome, e-mail e senha). |
| RF03 | O sistema deve permitir cadastrar, editar, buscar e excluir clientes. |
| RF04 | O sistema deve permitir cadastrar, editar, desativar e excluir serviços. |
| RF05 | O sistema deve permitir criar e editar agendamentos (cliente, serviço, data/hora, observação). |
| RF06 | O sistema deve permitir concluir ou cancelar um agendamento. |
| RF07 | O sistema deve exibir a agenda de qualquer dia escolhido. |
| RF08 | O sistema deve exibir um painel com atendimentos do dia, total de clientes, serviços ativos, faturamento do dia e próximos atendimentos. |

## 1.7 Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Interface em português, responsiva (funciona em celular). |
| RNF02 | Senhas armazenadas com *hash* (nunca em texto puro). |
| RNF03 | Formulários protegidos contra CSRF. |
| RNF04 | Mensagens de erro claras, sem expor detalhes técnicos. |
| RNF05 | Código organizado no padrão MVC e versionado no GitHub. |
| RNF06 | Regras de negócio cobertas por testes automatizados (pytest). |
| RNF07 | Datas e horários sempre no fuso do salão (America/Sao_Paulo), independentemente do fuso do servidor. |

## 1.8 Regras de negócio

| ID | Regra |
|---|---|
| RN01 | Não pode haver dois agendamentos **em aberto** com horários sobrepostos. |
| RN02 | Não é permitido agendar em data/hora passada. |
| RN03 | O atendimento deve começar e terminar entre 08h e 20h, de segunda a sábado. |
| RN04 | O horário de término é calculado: início + duração do serviço. |
| RN05 | Somente serviços ativos podem ser agendados. |
| RN06 | Somente agendamentos "agendado" podem ser editados, concluídos ou cancelados. |
| RN07 | Cliente com agendamentos não pode ser excluído. |
| RN08 | O telefone do cliente é obrigatório, único e deve ter DDD + número (10 ou 11 dígitos). |
| RN09 | A senha deve ter no mínimo 6 caracteres; o e-mail do usuário é único. |
| RN10 | Limites de tamanho: nomes de pessoa até 100 caracteres, nome de serviço até 80, e-mail até 120; preço até R$ 999.999,99. |
| RN11 | Na edição de um agendamento, o horário original pode ser mantido mesmo que já tenha passado. |
