---
name: hld
description: Entrevista para escrever ou revisar o High-Level Design do Nextflow (módulos, containers, infraestrutura, integrações); use ao mexer em architecture-overview.md ou integrations/.
---

# HLD por entrevista

Saída: `docs/architecture/architecture-overview.md` e, quando houver terceiro novo, `docs/architecture/integrations/<nome>.md`.

## Roteiro
1. Contexto: quem usa, quais sistemas externos (confirme a lista atual: PostgreSQL, storage S3, Gemini, ViaCEP).
2. Módulos: responsabilidades e dependências; confirme a divisão de `product-overview.md` §5.
3. Ambientes: dev, staging, produção (existe?); onde roda, como sobe, quem acessa.
4. Atributos de qualidade com número: desempenho, disponibilidade, backup, segurança, LGPD.
5. Riscos técnicos e decisões que viram ADR.

## Regras
- Uma pergunta de cada vez quando a resposta muda a arquitetura; recomende sempre uma opção.
- Diagramas em Mermaid (use as skills `c4` e `mermaid`).
- Detalhe de classe ou rota não entra no HLD: aponte para os docs dos repositórios.
- Cada integração tem contrato: para que serve, endpoint, autenticação, limites, o que acontece quando falha.
