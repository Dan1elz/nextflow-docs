# 0007 — Estoque como livro-razão com um único dono

> **Status:** proposta · **Data:** 2026-10-28 · **Origem:** entrevista de estoque com o Daniel ("não pode virar ninho de rato")

## Contexto
Hoje vendas, compras e ajustes gravam movimentações e alteram `Product.Quantity` cada um do seu jeito.

## Decisão
`stock_movements` é um livro-razão imutável (erro se corrige com movimento contrário). `stock_balances` é o saldo
materializado, atualizado na mesma transação, com controle de concorrência. Só o módulo de estoque grava nessas tabelas,
por um único serviço (`IStockLedger`); vendas, compras, transferências e inventário chamam esse serviço.

## Consequências
- Histórico confiável para a sazonalidade e auditoria.
- Refatoração de `CreateOrderUseCase`, `UpdateStatusByOrderIdUseCase`, `UpdatePurchaseOrderUseCase` e `CreateStockMovementUseCase`.
