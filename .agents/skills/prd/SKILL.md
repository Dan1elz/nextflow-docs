---
name: prd
description: Entrevista o Daniel para construir ou revisar a visão de produto e os requisitos (PRD) do Nextflow; use ao mexer em product-overview.md, escopo, público, objetivos ou regras de negócio.
---

# PRD por entrevista

Objetivo: produzir ou atualizar `docs/product-overview.md` e os `business-rules.md` a partir das respostas do Daniel,
não da imaginação do agente.

## Antes de perguntar
1. Leia `docs/product-overview.md` e a seção "Perguntas em aberto" do documento em foco. Não releia o TCC inteiro.
2. Faça a pesquisa de mercado você mesmo (o Daniel é dev e não conhece o mercado): traga dados e exemplos de concorrentes.

## Como entrevistar
- **Uma etapa por vez**, no máximo 3 a 5 perguntas por rodada, cada uma com **uma recomendação** e o porquê.
- Questione: se a resposta contradiz outra decisão, aponte a contradição. O Daniel quer pensar junto.
- Ordem das etapas: (1) problema e público, (2) objetivo e métrica de sucesso, (3) escopo dentro/fora,
  (4) jornadas principais, (5) regras de negócio por módulo, (6) riscos e premissas.
- Prefira perguntas fechadas com opções ("A, B ou C? Recomendo B porque…").

## Como registrar
- Atualize o documento logo após cada rodada, com a data da resposta.
- Resposta que vira regra: linha nova no `business-rules.md` com ID, fonte ("entrevista AAAA-MM-DD") e status `validado`.
- Resposta que é escolha entre alternativas: crie uma decisão numerada (template `0000-template.md`).
- O que ficou sem resposta continua em "Perguntas em aberto".
