# Roteiros dos Vídeos

**Ferramentas:** OBS Studio (grátis), Xbox Game Bar no Windows (`Win + Alt + R`) ou Loom. Grave a tela com o microfone ligado; não é obrigatório aparecer.
**Publicação:** YouTube como **"Não listado"** (ou Google Drive com "qualquer pessoa com o link"). Teste o link numa aba anônima antes de entregar.

**Antes de gravar:** deixe abertas três abas — o repositório no GitHub, o sistema publicado (já logado) e o VS Code com o projeto. Cadastre previamente 2 serviços e 2 clientes para o vídeo fluir.

---

## Vídeo 1 – Apresentação da solução (mínimo 5 minutos)

### 0:00 – Abertura (≈ 30 s) · *tela: página inicial do GitHub*
> "Olá, meu nome é ___, RGM ___. Este é o AgendaFácil, projeto do Projeto Integrador Transdisciplinar em Engenharia de Software II. É um sistema web de agendamento para salões de beleza."

### 0:30 – Problema e objetivo (≈ 40 s) · *tela: README*
> "Muitos salões ainda controlam horários em caderno ou pelo WhatsApp, o que causa horário marcado em duplicidade e falta de controle. O AgendaFácil organiza clientes, serviços e a agenda, e impede que dois atendimentos sejam marcados no mesmo horário. O código e a documentação foram desenvolvidos com apoio da ferramenta de IA Claude."

### 1:10 – Documentação e tecnologias (≈ 1 min) · *tela: pasta docs no GitHub*
> "No repositório, a documentação está separada por situação. Na situação 1 estão o escopo, os requisitos, os diagramas UML — casos de uso, classes, sequência e atividades — e o projeto do banco com o dicionário de dados."
*(abra o 03-banco-de-dados.md e mostre o DER)*
> "O back-end é em Python com Flask, no padrão MVC. O banco é SQLite, acessado pelo SQLAlchemy. O front-end usa HTML, CSS e JavaScript, e o sistema está hospedado no PythonAnywhere."

### 2:10 – Código MVC (≈ 50 s) · *tela: VS Code*
> "Na pasta models ficam as regras de negócio."
*(abra `agendamento.py` e mostre o método `preencher`)*
> "Aqui o sistema calcula o fim do atendimento e verifica se o horário está no passado, fora do expediente, num domingo ou em conflito com outro agendamento. Os controllers recebem as requisições e as views são as telas."

### 3:00 – Demonstração (≈ 2 min 30 s) · *tela: sistema publicado*
1. Mostre o **login** e o **Painel**. > "Ao entrar, o painel mostra os atendimentos do dia, os clientes, os serviços ativos e o faturamento."
2. **Serviços:** cadastre um novo. > "Cada serviço tem duração, que é usada para calcular o horário de término."
3. **Clientes:** digite um telefone errado e mostre o erro; depois cadastre certo. Use a busca.
4. **Agenda:** crie um agendamento às 10h. Depois tente outro às 10h30 e mostre a mensagem de **conflito**. Tente um domingo.
5. **Concluir** um atendimento e mostrar no Painel o faturamento atualizado. **Cancelar** outro e mostrar que o horário ficou livre.
6. Abra no **celular** (ou reduza a janela) e mostre o layout responsivo.

### 5:30 – Testes automatizados (≈ 30 s) · *tela: terminal*
Rode `python -m pytest -v`.
> "O projeto tem 54 testes automatizados com pytest, cobrindo as regras de negócio, as telas e as correções feitas depois dos testes. Todos passaram."

### 6:00 – Encerramento (≈ 20 s)
> "Esse foi o AgendaFácil. Os links do repositório e do sistema estão na entrega. Obrigado(a)!"

---

## Vídeo 2 – Correções após os testes (até 5 minutos)

> Preencha os colchetes com os problemas reais apontados pelos colegas, na mesma ordem do Laudo de Qualidade.

### 0:00 – Abertura (≈ 20 s)
> "Olá, sou ___, RGM ___. Neste vídeo mostro as correções feitas no AgendaFácil depois dos testes com cinco colegas."

### 0:20 – Testes exploratórios (≈ 1 min) · *tela: laudo de qualidade no GitHub*
> "Antes de enviar para os colegas, fiz uma rodada de testes tentando quebrar o sistema e encontrei 8 erros. Os dois mais graves: qualquer pessoa conseguia criar uma conta e ver os clientes do salão, e o servidor de hospedagem, que fica em outro fuso horário, recusava horários de hoje como se já tivessem passado."
*(mostre os prints `E01` e `E04` antes e depois, e demonstre no sistema publicado: abra /cadastro sem login e marque um horário para daqui a uma hora)*
> "Os dois foram corrigidos, assim como os outros seis, e cada correção ganhou um teste automatizado."

### 1:20 – Como foi o teste dos colegas (≈ 30 s) · *tela: formulário / laudo*
> "Enviei o link do sistema e um roteiro de tarefas para cinco colegas. Eles responderam um formulário dizendo o que funcionou, o que não funcionou e o que não testaram. No total foram apontados [N] problemas e [N] sugestões."

### 1:50 – Correções apontadas pelos colegas (≈ 2 min, ~40 s por item) · *para cada item:*
> "O [colega] apontou que [problema]."
*(mostre o print "antes")*
> "A correção foi [o que mudou]."
*(mostre o trecho do código ou o commit no GitHub)*
> "Agora funciona assim:" *(demonstre no sistema publicado)*

### 4:00 – O que ficou para depois (≈ 30 s)
> "As sugestões [X] e [Y] ficaram para a próxima versão, porque [motivo]."

### 4:30 – Encerramento (≈ 20 s)
> "Todas as mudanças estão registradas no laudo de qualidade dentro do repositório. Obrigado(a)!"
