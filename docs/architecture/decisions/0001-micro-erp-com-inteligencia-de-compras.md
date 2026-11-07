# 0001 — Posicionamento: micro ERP com inteligência de compras

> **Status:** decidido (rascunho) · **Data:** 2026-10-27 · **Quem decidiu:** Daniel
> **Origem:** conversa de escopo do projeto (27/10/2026)

## Contexto
O texto do TCC descreve um "software modular de gestão de estoques adaptável a qualquer empresa". Na prática, o código
cobre produtos, estoque, vendas e compras, e o diferencial construído foi a previsão de demanda sazonal com IA.

## Decisão
O Nextflow nasce como **micro ERP focado em gestão de produtos e vendas**, com **inteligência de compras** (previsão sazonal
com IA) como diferencial. ERP completo (CRM, finanças, multi-tenant) é futuro, fora do TCC.

## Consequências
- O texto do TCC precisa ser ajustado a esse foco.
- Itens do diagrama de visão (CRM, finanças, permissões) vão para "Trabalhos futuros".

## Perguntas em aberto
- Público-alvo ainda indefinido (hipótese: varejo físico sazonal).

## Atualização 2026-10-28
Público definido pelo Daniel: empresas de 4 a 15 funcionários, de qualquer tipo de comércio. A sazonalidade com IA é o
diferencial principal; o produto (catálogo e estoque) é estruturado para alimentar essa análise.
