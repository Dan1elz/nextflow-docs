# 0005 — Backend calcula, IA interpreta, humano decide

> **Status:** rascunho / a validar · **Data:** 2026-10-11 · **Quem decidiu:** Daniel (na especificação do módulo)
> **Origem:** `nextflow/docs/AI_FORECAST_SPEC.md` §1 e §6

## Contexto
Modelos generativos erram números e não são reproduzíveis. A banca e o usuário precisam entender de onde vem cada sugestão.

## Decisão
Todos os números da previsão vêm de cálculo determinístico (`ForecastCalculator`). A IA (Gemini, atrás de `IAiClient`)
só prioriza e explica, dentro de guardrails. Sem IA disponível, o sistema funciona só com o cálculo
(`CompletedWithoutAi`). Nenhuma ação é executada sem clique.

## Consequências
- Trocar de provedor de IA mexe só na implementação de `IAiClient`.
- A previsão é testável e explicável no TCC.
