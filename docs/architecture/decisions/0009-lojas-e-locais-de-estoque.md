# 0009 — Lojas e locais de estoque

> **Status:** decidido (rascunho) · **Data:** 2026-10-28 · **Quem decidiu:** Daniel (RN-CE12, RN-CE13, RN-CE33)

## Contexto
Comércios de 4 a 15 funcionários costumam ter loja e depósito, ou mais de uma loja. O "local de estoque" estava em aberto no diagrama antigo.

## Decisão
Loja = onde se vende; local = onde a mercadoria fica (prateleira, depósito). Saldo por variação × local × lote. Compra
informa o local de entrega, venda informa a loja/local de baixa, remanejamento por transferência. A IA pode recomendar
transferir antes de comprar. Empresa com uma loja só tem loja e local padrão, invisíveis até cadastrar o segundo local.
Só a visão do Admin por enquanto.
