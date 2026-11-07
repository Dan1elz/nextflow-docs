# 0008 — Variação é a unidade de estoque, venda e compra

> **Status:** decidido (rascunho) · **Data:** 2026-10-28 · **Quem decidiu:** Daniel (RN-CE09, RN-CE11, RN-CE34)

## Contexto
Para atender qualquer comércio (roupa com grade), o estoque precisa ser por tamanho/cor.

## Decisão
Todo produto tem ao menos uma variação (padrão oculta quando não há grade). Estoque, itens de venda, itens de compra e
promoções apontam para a variação. A previsão é por produto e é rateada nas variações pela proporção histórica.

## Consequências
- Maior mudança de código do ciclo: pedidos, compras, previsão e seed de demonstração. Feita junto com o estoque.
