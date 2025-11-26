# ADR 001 - Escolha do banco de dados Supabase para o projeto

**Data:** 2025-11-11  
**Status:** Aceita  
**Autores:** Squad de Backend  

---

## Contexto
A equipe está desenvolvendo a **plataforma digital do EduTech**, que exige um banco de dados acessível e de fácil integração para todos os membros do squad.  
Como o desenvolvimento ocorre de forma **remota**, com cada integrante trabalhando a partir de sua própria máquina, era necessário um banco que permitisse **acesso centralizado e estável pela internet**, sem depender de um servidor local configurado internamente.

O **Supabase** foi considerado uma solução adequada, pois oferece um **servidor externo pronto**, eliminando a necessidade de montar e manter uma infraestrutura própria apenas para compartilhamento de dados entre os desenvolvedores.

---

## Decisão
Foi decidido que o **Supabase** será utilizado como **banco de dados principal** da plataforma EduTech.  
A escolha se baseou principalmente no fato de ser uma **solução open source** que oferece um **ambiente remoto acessível** para toda a equipe, permitindo consultas e atualizações de forma integrada, sem necessidade de configuração de servidores locais.

Nesta etapa do projeto, o Supabase será utilizado **apenas para a hospedagem e gerenciamento do banco de dados PostgreSQL**, sem o uso de outras funcionalidades adicionais oferecidas pela plataforma (como autenticação, armazenamento de arquivos ou APIs automáticas).

---

## Alternativas Consideradas
- **Firebase (Google):** foi analisado por oferecer funcionalidades semelhantes e ampla documentação, mas descartado devido ao **risco de custos financeiros** que poderiam ser gerados com o uso de planos pagos ou aumento de tráfego, algo que a equipe não poderia arcar no momento.  

- **Bancos de dados locais (PostgreSQL, MySQL):** também foram considerados, porém exigiriam que cada membro do squad **mantivesse uma instância local sincronizada manualmente**, o que aumentaria a complexidade e poderia gerar **inconsistência nos dados e nos esquemas** entre diferentes ambientes de desenvolvimento.

---

## Consequências

**Positivas:**
- O Supabase garante um **fluxo de dados unificado** e atualizado em tempo real para todo o **squad de backend**, evitando divergências entre ambientes locais.  
- Permite que o **squad de frontend** também tenha **acesso transparente** ao banco, facilitando testes e validações durante o desenvolvimento.  
- Reduz a complexidade da infraestrutura, eliminando a necessidade de manutenção de servidores locais e simplificando a colaboração remota.

**Negativas:**
- A equipe ainda **não possui domínio técnico completo** sobre o Supabase, o que pode gerar dependência de aprendizado inicial.  
- Há risco de **exposição indevida da API key**, que concederia acesso direto ao banco de dados; portanto, será necessário garantir que essas chaves fiquem **armazenadas de forma segura** (por exemplo, em variáveis de ambiente).  
- Dependência de um **serviço externo**, o que pode causar **downtime** (períodos de indisponibilidade) em caso de falhas nos servidores ou limitações do plano gratuito.

**Mitigação:**
- Serão realizados **backups periódicos do banco de dados** para preservar a integridade das informações em caso de falhas.  
- As **API keys** serão armazenadas em **variáveis de ambiente seguras** e nunca incluídas em repositórios públicos.  
- Em caso de interrupção temporária, a equipe poderá utilizar uma **cópia local exportada** dos dados essenciais para continuar testes ou validações críticas.
