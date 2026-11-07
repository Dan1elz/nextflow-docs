# 0001 — Compra recebida não cancela; sem recebimento parcial

> **Status:** decidido (rascunho) · **Data:** 2026-10-27 · **Quem decidiu:** Daniel
> **Origem:** review de código e QA de 27/10/2026 (doc "Nextflow — achados e decisões do review", decisão R5)

## Contexto
O QA testou cancelar compra já recebida e receber parte dos itens; o comportamento era inconsistente.

## Decisão
Pedido de compra **recebido não pode ser cancelado**. Não há **recebimento parcial**: o pedido é recebido inteiro.

## Consequências
- Divergência na entrega (faltou item) se resolve com ajuste de estoque ou novo pedido.
- Simplifica o cálculo de lead time e de estoque a chegar.
