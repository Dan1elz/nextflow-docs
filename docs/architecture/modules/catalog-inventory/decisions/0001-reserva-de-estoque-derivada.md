# 0001 — Reserva de estoque derivada, com validade de orçamento

> **Status:** decidido (rascunho) · **Data:** 2026-10-27 · **Quem decidiu:** Daniel
> **Origem:** review de código e QA de 27/10/2026 (doc "Nextflow — achados e decisões do review", decisão R7)

## Contexto
Hoje o orçamento não reserva nada e o estoque só baixa no pagamento; dois orçamentos podem prometer o mesmo item.

## Decisão
- Separar **estoque físico** e **estoque disponível**.
- Orçamento passa a ter **validade** (7 dias, **provisório**).
- A reserva é **calculada** (soma dos itens de orçamentos/pedidos válidos), não gravada como movimentação.
- O estoque físico só baixa quando o pagamento é confirmado.

## Consequências
- Orçamento vencido deixa de reservar sem precisar de job.
- A previsão deve decidir se usa físico ou disponível (pergunta em aberto no módulo de previsão).

## Perguntas em aberto
- Validade configurável por loja ou por orçamento?
- Pedido "aguardando pagamento" reserva sem prazo?
