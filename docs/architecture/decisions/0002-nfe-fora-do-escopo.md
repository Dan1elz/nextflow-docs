# 0002 — NF-e e NFC-e fora do escopo

> **Status:** decidido (rascunho) · **Data:** 2026-10-27 · **Quem decidiu:** Daniel
> **Origem:** conversa de escopo do projeto (27/10/2026)

## Contexto
Emissão fiscal exige certificado digital, integração com SEFAZ por estado e regras tributárias extensas. O TCC citava a
leitura de XML de notas como trabalho futuro.

## Decisão
O sistema não emite nem importa NF-e/NFC-e.

## Consequências
- Venda no Nextflow não substitui o emissor fiscal da loja.
- Entrada de estoque continua manual ou via pedido de compra recebido.

## Perguntas em aberto
- Importar XML de NF-e de compra (entrada de estoque) continua como futuro?
