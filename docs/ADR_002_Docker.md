# ADR 002 - Adoção do Docker no desenvolvimento

**Data:** 2025-11-11  
**Status:** Aceita  
**Autores:** Squad de Backend  

---

## Contexto
Durante o desenvolvimento remoto da **plataforma digital do EduTech**, cada integrante do squad utiliza uma máquina com configurações e sistemas operacionais diferentes.  
Essa variação gerava o risco de **inconsistências no ambiente de desenvolvimento**, dificultando a replicação das dependências e a execução uniforme do backend entre os membros da equipe.  

O uso do **Docker** foi considerado uma solução para **padronizar o ambiente de desenvolvimento**, garantindo que o backend seja executado da mesma forma em todas as máquinas, independentemente do sistema operacional ou especificações de hardware.

---

## Decisão
Foi decidido que o **Docker** será utilizado como **ferramenta principal de ambiente de desenvolvimento** do backend.  
A escolha foi motivada pela capacidade do Docker de **criar um ambiente comum e reproduzível**, garantindo que todos os desenvolvedores utilizem as **mesmas versões de software e bibliotecas**.  

A equipe optou por utilizar o **Docker Compose** para orquestrar os containers e um **Makefile** para automatizar o processo de inicialização e configuração do ambiente, simplificando a execução dos serviços e reduzindo erros manuais de configuração.  

O ambiente Docker permitirá a utilização de **Docker Secrets** para o armazenamento seguro de **API keys sensíveis**, como as chaves do Supabase.  
Também fará uso de **volumes** para **preservar dados persistentes fora dos containers**, assegurando que informações críticas permaneçam disponíveis mesmo após reinicializações.

---

## Alternativas Consideradas
Não foram consideradas outras ferramentas além do **Docker**, pois desde o início a equipe identificou que o uso de **máquinas virtuais (VMs)** seria uma solução **mais complexa e difícil de manter**.  
O Docker, por outro lado, oferecia **maior simplicidade e replicabilidade** do ambiente de desenvolvimento em diferentes máquinas.

Além disso, parte da equipe já possuía **familiaridade prévia com o Docker**, o que tornava sua adoção mais natural.  
Os membros que ainda não tinham experiência também não possuíam conhecimento avançado em VMs, o que reforçou a decisão de optar pelo Docker como opção mais acessível e prática para todos.

---

## Consequências

**Positivas:**
- O Docker facilita a **replicação e manutenção do ambiente de desenvolvimento**, permitindo ajustes e atualizações rápidas sem comprometer a configuração dos demais membros da equipe.  
- Garante **uniformidade na execução do backend**, evitando erros de dependência e incompatibilidades entre diferentes máquinas.  
- Simplifica o **onboarding de novos desenvolvedores**, que podem iniciar o ambiente local com um único comando, reduzindo o tempo de configuração.  
- O uso de **um container único** para o backend reduz a complexidade da configuração, mantendo o ambiente leve e de fácil manutenção.

**Negativas:**
- Pode haver **pequena perda de desempenho** em máquinas com hardware mais limitado, devido à execução do ambiente em container.  
- Exige **conhecimento básico de Docker** para criação, build e execução das imagens, o que pode gerar uma curva de aprendizado inicial.  
- A configuração incorreta do container pode gerar **erros de permissão ou volume**, exigindo atenção na documentação de setup.

**Mitigação:**
- Serão criados **scripts automatizados e instruções documentadas** no repositório para facilitar a configuração e execução do container via Makefile.  
- A equipe manterá uma **documentação padronizada** sobre o uso do Docker e sobre o processo de build do container.  
- Caso ocorram problemas de desempenho, será avaliada a possibilidade de **otimização da imagem base** ou ajustes de recursos alocados.
