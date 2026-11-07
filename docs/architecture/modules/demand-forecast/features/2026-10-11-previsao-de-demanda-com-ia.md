# 2026-10-11 — Previsão de demanda com IA (primeira versão)

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** `AI_FORECAST_SPEC.md`, `PROJECT.md` (branch `task-17`, não commitada)

## O que entrou
- Schema: promoções, agregados mensais de venda, sazonalidade, análises, recomendações e projeções (migration `AddAiForecastModule`).
- Preço efetivo com promoção vigente em pedidos e produtos.
- Motor de cálculo, cliente Gemini, guardrails, rotas `/api/forecasts` e `/api/promotions`.
- Front: card no dashboard, página `/forecast`, `/promotions`, aba "Previsão" do produto.
- Seed de demonstração: loja de doces e presentes, 48 SKUs, 36 meses (atualizado em 27/10/2026).

## Estado
Validado ponta a ponta em 11/10/2026; sem commit em 28/10/2026.
