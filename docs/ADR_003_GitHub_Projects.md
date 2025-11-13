# ADR 003 - GitHub Projects como gerenciador de tarefas

**Data:** 2025-11-11  
**Status:** Aceita  
**Autores:** Squad de Backend  

---

## Contexto
A equipe precisava de uma ferramenta centralizada para **anotar o backlog**, **organizar as tarefas** e **acompanhar o andamento** de cada atividade junto com o responsável designado.  

Como o desenvolvimento do projeto é hospedado no **GitHub**, a escolha de uma solução integrada ao próprio repositório se mostrou mais eficiente.  
O **GitHub Projects** oferece integração direta com **issues**, **pull requests** e **commits**, permitindo que o acompanhamento do progresso ocorra de forma automatizada e alinhada ao fluxo de versionamento.

---

## Decisão
Foi definido que o **GitHub Projects** será a **ferramenta oficial de gerenciamento de tarefas** da squad.  
O board será estruturado em colunas que representam o fluxo de trabalho: **Backlog**, **Ready**, **In Progress**, **In Review** e **Done**.  

A escolha pelo GitHub Projects se deu pela **integração nativa com o repositório**, permitindo vincular **issues** e **pull requests** diretamente ao projeto.  
Quando uma issue ou PR é encerrada, o GitHub atualiza automaticamente o seu status no board, movendo-a para a coluna **Done**.  
Essa automação reduz o esforço manual de controle e garante **visibilidade em tempo real** do progresso da equipe.

---

## Alternativas Consideradas
- **Jira:** foi cogitado por ser amplamente utilizado em equipes de desenvolvimento, mas descartado devido à **falta de familiaridade da equipe** com a ferramenta.  
A maioria dos integrantes já possuía **experiência prévia sólida com o GitHub Projects**, o que tornava o uso do Jira menos prático no contexto do projeto.  

- **Notion:** é utilizado pelo grupo para **documentação técnica e administrativa**, mas não foi escolhido para a gestão de tarefas para evitar **mistura de fluxos** e **dificuldades na organização** das páginas.  

- **Trello:** não chegou a ser considerado, pois o GitHub Projects já atendia plenamente às necessidades da equipe e oferecia **integração direta com o repositório**.

---

## Consequências

**Positivas:**
- O uso do **GitHub Projects** centraliza a **gestão de tarefas e o controle de progresso** dentro do mesmo ambiente de desenvolvimento.  
- As **integrações automáticas com issues e pull requests** reduzem o esforço manual de atualização e garantem rastreabilidade completa das entregas.  
- Melhora a **visibilidade do andamento do projeto** para todos os membros da squad, facilitando a priorização e distribuição de tarefas.  
- A interface simples e a familiaridade da equipe com o GitHub tornam o gerenciamento mais **rápido e intuitivo**.

**Negativas:**
- O GitHub Projects possui **limitações de personalização** em comparação a ferramentas mais robustas, como o Jira.  
- Há uma **dependência total da plataforma GitHub** — caso o serviço apresente instabilidade, o acesso ao board também é afetado.  
- Algumas métricas de acompanhamento (como gráficos de burndown ou relatórios avançados) exigem **configurações manuais** ou integrações externas.

**Mitigação:**
- A equipe manterá **revisões periódicas do board** para garantir que o fluxo de tarefas continue eficiente.  
- Caso surjam novas demandas de métricas ou relatórios, serão avaliadas **integrações adicionais com o GitHub Insights ou ferramentas externas**, sem comprometer a simplicidade do processo.
