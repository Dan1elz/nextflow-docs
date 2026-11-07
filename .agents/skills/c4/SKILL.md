---
name: c4
description: Cria ou revisa diagramas C4 (contexto, containers, componentes) do Nextflow em Mermaid; use ao documentar arquitetura em docs/architecture/diagrams.
---

# Diagramas C4

Saída: `docs/architecture/diagrams/c4-<nivel>-<nome>.md`, com o bloco Mermaid e uma legenda curta.

## Níveis
1. **Contexto**: pessoas e sistemas externos (Admin da loja, Gemini, ViaCEP, storage).
2. **Containers**: SPA, API, PostgreSQL, storage, proxy de borda.
3. **Componentes**: por container, só quando ajudar (ex.: camadas da API, motor de previsão).

## Regras
- Confirme com o Daniel, em uma pergunta, o público do diagrama (banca, dev, QA) antes de escolher o nível.
- Use `flowchart` do Mermaid (mais portátil que a sintaxe `C4Context`, que nem todo visualizador renderiza).
- Cada caixa: nome, tecnologia e responsabilidade em uma linha. Cada seta: o que trafega e o protocolo.
- Atualize a tabela de `docs/architecture/diagrams/README.md`.
