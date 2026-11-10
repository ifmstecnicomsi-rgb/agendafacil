# Testes Automatizados (verificação)

Ferramenta: **pytest** (equivalente em Python ao JUnit/PHPUnit). Banco usado nos testes: SQLite em memória, recriado a cada teste.

```bash
python -m pytest -v
```

**Resultado (versão 1.1): 54 testes executados, 54 aprovados, 0 falhas.** (Versão 1.0: 40 testes.)

## Testes unitários – `tests/test_models.py` (regras de negócio)

| Caso de teste | Regra verificada | Resultado esperado |
|---|---|---|
| test_cadastrar_usuario_e_autenticar | RF01/RF02 | Login aceita a senha correta e recusa a errada |
| test_senha_curta_rejeitada | RN09 | Senha com menos de 6 caracteres é recusada |
| test_email_duplicado_rejeitado | RN09 | E-mail já usado é recusado |
| test_senha_armazenada_com_hash | RNF02 | Senha não é gravada em texto puro |
| test_telefone_normalizado_e_formatado | RN08 | "(61) 99999-1234" vira "61999991234" e é exibido formatado |
| test_telefone_invalido (4 variações) | RN08 | Telefones curtos, longos ou vazios são recusados |
| test_telefone_duplicado | RN08 | Telefone repetido é recusado |
| test_email_cliente_invalido | RF03 | E-mail mal formatado é recusado |
| test_busca_cliente_por_nome | RF03 | Busca encontra por nome (sem diferenciar maiúsculas) |
| test_servico_preco_formatado | RF04 | Preço exibido como "R$ 80,00" |
| test_servico_duracao_invalida (3 variações) | RF04 | Duração 0, 1000 ou texto é recusada |
| test_servico_preco_negativo | RF04 | Preço negativo é recusado |
| test_agendamento_calcula_fim | RN04 | Fim = início + duração |
| test_agendamento_no_passado | RN02 | Data passada é recusada |
| test_agendamento_fora_do_horario | RN03 | Início às 07h e término às 20h30 são recusados |
| test_agendamento_no_domingo | RN03 | Domingo é recusado |
| test_conflito_de_horario | RN01 | Sobreposição de horários é recusada |
| test_horario_encostado_nao_conflita | RN01 | 10h–11h e 11h–12h são aceitos (sem sobreposição) |
| test_cancelado_libera_horario | RN01/RF06 | Após cancelar, o horário pode ser reutilizado |
| test_nao_altera_status_finalizado | RN06 | Concluído não pode ser cancelado |
| test_servico_inativo_nao_agenda | RN05 | Serviço inativo não pode ser agendado |
| test_data_texto_invalida | RF05 | Data em formato inválido é recusada |

## Testes de integração – `tests/test_rotas.py` (Controller + View + banco)

| Caso de teste | Fluxo verificado | Resultado esperado |
|---|---|---|
| test_redireciona_para_login_sem_sessao | Segurança | Sem login, o usuário é enviado à tela de login |
| test_login_invalido | RF01 | Mensagem "E-mail ou senha incorretos" |
| test_login_valido_abre_painel | RF01/RF08 | Painel exibido |
| test_cadastro_de_usuario | RF02 | Usuário logado cadastra outro usuário |
| test_cadastro_senhas_diferentes | RF02 | Mensagem "senhas não conferem" |
| test_crud_cliente | RF03 | Cria, edita e exclui cliente pela interface |
| test_cliente_invalido_mostra_erro_e_mantem_dados | RNF04 | Mensagem de erro e o nome digitado continua no campo |
| test_cliente_inexistente_404 | Tratamento de erro | Página 404 |
| test_crud_servico | RF04 | Serviço criado e ativo |
| test_fluxo_completo_de_agendamento | RF05/RF06/RN01/RN06 | Agenda, detecta conflito, conclui e bloqueia edição |
| test_cliente_com_agendamento_nao_exclui | RN07 | Exclusão bloqueada com mensagem |
| test_agenda_data_invalida | Tratamento de erro | Aviso "Data inválida" e exibe hoje |
| test_logout | RF01 | Após sair, rotas internas exigem login |

## Testes de regressão – `tests/test_correcoes_v11.py` (versão 1.1)

Cada teste reproduz um erro encontrado nos testes exploratórios (ver [Laudo de Qualidade](laudo-de-qualidade.md)) e confirma a correção.

| Caso de teste | Erro | Resultado esperado |
|---|---|---|
| test_e01_visitante_nao_cadastra_usuario | E01 | Visitante sem login é enviado ao login e nenhum usuário é criado |
| test_e02_pagina_405_em_portugues | E02 | Página 405 própria, em português |
| test_e03_nome_cliente_muito_longo | E03 | Nome com mais de 100 caracteres é recusado |
| test_e03_nome_servico_muito_longo | E03 | Nome de serviço com mais de 80 caracteres é recusado |
| test_e04_agora_usa_fuso_do_salao_mesmo_com_servidor_em_utc | E04 | Com o servidor em UTC, `agora()` continua no horário de Brasília |
| test_e05_editar_observacao_de_horario_passado | E05 | Permite salvar mantendo um horário que já passou |
| test_e05_mudar_para_horario_passado_continua_bloqueado | E05 | Mudar para um horário passado continua proibido |
| test_e06_moeda_com_separador_de_milhar | E06 | 1500 → "R$ 1.500,00" |
| test_e07_preco_formato_brasileiro (5 variações) | E07 | "1.234,56", "80,50", "80", "R$ 35,00" e "99.9" convertidos corretamente |
| test_e08_preco_acima_do_limite | E08 | Preço acima de R$ 999.999,99 é recusado |

## Testes manuais de interface (validação)

Executados no navegador (desktop 1200 px e celular 390 px), com evidências em `docs/situacao-2-codificacao/telas/`:

| Teste | Resultado | Evidência |
|---|---|---|
| Login com usuário padrão | OK | 1_login.png |
| Cadastro de dois serviços | OK | 2_servicos.png |
| Telefone inválido bloqueado no navegador | OK | 3_validacao.png |
| Cadastro de cliente com máscara de telefone | OK | 4_clientes.png |
| Agendamento salvo e exibido na agenda | OK | 5_agenda.png |
| Agendamento sobreposto bloqueado com mensagem | OK | 6_conflito.png |
| Painel com indicadores e próximos atendimentos | OK | 7_painel.png |
| Layout no celular | OK | 8_mobile.png |

Os testes de aceitação feitos pelos **5 colegas** estão no [Laudo de Qualidade](laudo-de-qualidade.md).
