# 0003 — Promoção abaixo do custo: avisa e confirma

> **Status:** decidido (rascunho) · **Data:** 2026-10-27 · **Quem decidiu:** Daniel
> **Origem:** review de código e QA de 27/10/2026 (doc "Nextflow — achados e decisões do review", decisão R4)

## Contexto
A promoção manual não considera o custo; a sugerida pela previsão preserva 10% de margem. Queima de estoque abaixo do
custo às vezes é desejada (ex.: validade vencendo).

## Decisão
Se o preço promocional ficar **abaixo do custo**, o sistema **avisa** e pede **confirmação**; não bloqueia.

## Consequências
- Exige `CostPrice` preenchido para avisar; sem custo, não há aviso (a validar).
