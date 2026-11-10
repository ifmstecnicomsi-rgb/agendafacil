# 2. Modelagem UML (revisada)

> Os diagramas estão em **Mermaid** e aparecem desenhados automaticamente no GitHub.

## 2.1 Diagrama de casos de uso

```mermaid
flowchart LR
    A((Atendente))
    subgraph AgendaFácil
      UC1([Fazer login / logout])
      UC2([Cadastrar usuário da equipe])
      UC3([Manter clientes])
      UC4([Buscar cliente])
      UC5([Manter serviços])
      UC6([Agendar atendimento])
      UC7([Verificar conflito de horário])
      UC8([Concluir / cancelar atendimento])
      UC9([Consultar agenda do dia])
      UC10([Ver painel])
    end
    A --- UC1 & UC2 & UC3 & UC5 & UC6 & UC8 & UC9 & UC10
    UC3 -. include .-> UC4
    UC6 -. include .-> UC7
```

| Caso de uso | Descrição resumida |
|---|---|
| UC06 Agendar atendimento | O atendente escolhe cliente, serviço e data/hora. O sistema calcula o término, valida passado, expediente, domingo e conflito (UC07). Se tudo estiver certo, grava e mostra a agenda do dia; senão, exibe a mensagem do erro e mantém os dados preenchidos. |
| UC08 Concluir/cancelar | Disponível só para agendamentos em aberto. Cancelar libera o horário. |

## 2.2 Diagrama de classes (persistência)

```mermaid
classDiagram
    class Usuario {
      +int id
      +str nome
      +str email
      -str senha_hash
      +definir_senha(senha)
      +verificar_senha(senha) bool
      +cadastrar(nome, email, senha)$ Usuario
      +autenticar(email, senha)$ Usuario
    }
    class Cliente {
      +int id
      +str nome
      +str telefone
      +str email
      +datetime criado_em
      +telefone_formatado() str
      +preencher(nome, telefone, email)
      +pode_excluir() bool
      +buscar(termo)$ list
    }
    class Servico {
      +int id
      +str nome
      +int duracao_min
      +decimal preco
      +bool ativo
      +preco_formatado() str
      +preencher(nome, duracao, preco, ativo)
    }
    class Agendamento {
      +int id
      +datetime inicio
      +datetime fim
      +str status
      +str observacao
      +preencher(cliente, servico, inicio, obs)
      +alterar_status(novo)
      +do_dia(dia)$ list
    }
    Cliente "1" --> "0..*" Agendamento : possui
    Servico "1" --> "0..*" Agendamento : é usado em
```

## 2.3 Diagrama de sequência – Agendar atendimento

```mermaid
sequenceDiagram
    actor At as Atendente
    participant V as View (form.html)
    participant C as Controller (agendamentos)
    participant M as Model (Agendamento)
    participant BD as Banco SQLite
    At->>V: preenche cliente, serviço e data/hora
    V->>V: valida campos obrigatórios (JavaScript)
    V->>C: POST /agendamentos/novo
    C->>BD: busca Cliente e Servico
    C->>M: preencher(cliente, servico, inicio)
    M->>M: valida passado, expediente e domingo
    M->>BD: consulta agendamentos sobrepostos
    alt conflito ou regra violada
        M-->>C: ErroValidacao(mensagem)
        C-->>V: reexibe formulário com a mensagem
    else tudo válido
        C->>BD: INSERT agendamento
        C-->>V: redireciona para a agenda do dia
        V-->>At: "Agendamento salvo com sucesso."
    end
```

## 2.4 Diagrama de atividades – Ciclo do atendimento

```mermaid
flowchart TD
    I([Início]) --> A[Cliente pede horário]
    A --> B[Atendente abre Novo agendamento]
    B --> C{Cliente cadastrado?}
    C -- Não --> D[Cadastrar cliente] --> B
    C -- Sim --> E[Escolher serviço e horário]
    E --> F{Horário válido e livre?}
    F -- Não --> G[Sistema mostra o motivo] --> E
    F -- Sim --> H[Agendamento gravado: status 'agendado']
    H --> J{Dia do atendimento}
    J -- Compareceu --> K[Concluir: entra no faturamento]
    J -- Desmarcou --> L[Cancelar: horário liberado]
    K --> Z([Fim])
    L --> Z
```

## 2.5 Diagrama de estados – Agendamento

```mermaid
stateDiagram-v2
    [*] --> agendado
    agendado --> agendado : editar
    agendado --> concluido : concluir
    agendado --> cancelado : cancelar
    concluido --> [*]
    cancelado --> [*]
```
