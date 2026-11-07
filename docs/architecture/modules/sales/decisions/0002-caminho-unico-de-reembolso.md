# 0002 — Um único caminho de reembolso (Admin, até 7 dias)

> **Status:** decidido (rascunho) · **Data:** 2026-10-27 · **Quem decidiu:** Daniel
> **Origem:** review de código e QA de 27/10/2026 (doc "Nextflow — achados e decisões do review", decisão R3)

## Contexto
Hoje há dois caminhos com regras diferentes: excluir a venda (até 48 h) e estornar o pedido (até 7 dias após a última atualização).

## Decisão
Existe **um** caminho de reembolso, exclusivo do **Admin**, permitido até **7 dias**.

## Consequências
- Excluir venda deixa de existir como forma de reembolso.
- Precisa definir a data de referência dos 7 dias (pagamento é o mais natural).
