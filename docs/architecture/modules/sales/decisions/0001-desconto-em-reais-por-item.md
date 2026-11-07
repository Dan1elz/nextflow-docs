# 0001 — Desconto em reais por item

> **Status:** decidido (rascunho) · **Data:** 2026-10-27 · **Quem decidiu:** Daniel
> **Origem:** review de código e QA de 27/10/2026 (doc "Nextflow — achados e decisões do review", decisão R1)

## Contexto
O QA encontrou ambiguidade entre desconto percentual e em valor, e o total nem sempre refletia o desconto.

## Decisão
Desconto é um valor em **R$ por item** (`OrderItem.Discount`). O `TotalAmount` do pedido é **líquido** (já descontado).

## Consequências
- Desconto no total do pedido (no cabeçalho) não existe; se precisar, é rateado nos itens (a validar).
- O diagrama de visão tinha `TotalDiscount` no pedido: pode ser um campo calculado.
