# Módulo Catálogo e estoque — visão

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** `nextflow/docs/PROJECT.md`, `AI_FORECAST_SPEC.md` §3, TCC (RF001, RNF002), decisão R7 do review

## Desenho validado em 28/10/2026 (a implementar)
Entrevista com o Daniel (regras RN-CE09 a RN-CE34; DER em `../../diagrams/der-catalogo-v2-sazonalidade.md` e `der-catalogo-estoque.md`):
- **Produto → variação:** grade (tamanho, cor) com saldo próprio; produto sem grade tem variação padrão oculta. Venda e compra apontam para a variação.
- **Tipo de produto** (Padrão, Vestuário, Perecível, Granel) define padrões e campos da tela.
- **Lojas e locais:** a empresa tem lojas e locais (prateleira, depósito); saldo por variação × local × lote.
- **Lote e validade** opcionais por produto; baixa pelo lote que vence primeiro.
- **Livro-razão:** movimentações imutáveis; só o módulo de estoque grava saldo; transferência e inventário são documentos.
- **Custo médio** por variação; compra sempre na unidade de venda; estoque negativo bloqueado por padrão; mínimo por local.
- **Para a sazonalidade:** ciclo de vida, coleção, eventos, categoria em 2 níveis, produto × fornecedor, vida útil, política ABC,
  histórico de preço, venda em promoção marcada, dias sem estoque e demanda perdida.
- Só a visão do Admin por enquanto.

## O que faz hoje
Produtos (código, nome, marca, preço, custo, unidade, estoque mínimo, validade, imagem) em uma ou mais categorias.
O saldo de estoque é a **soma das movimentações** (entrada, saída, ajuste, venda, devolução). Movimentações de venda e
compra são geradas pelos módulos de vendas e compras; manualmente só entram entrada, saída e ajuste.

## Mudança decidida, ainda não implementada
Separar **estoque físico** de **estoque disponível** (físico − reservas de orçamentos válidos). Ver `decisions/0001`.

## Perguntas em aberto
- Local de estoque (várias lojas ou depósitos): a intenção original não é lembrada. Entra algum dia?
- Lote e validade por lote? Hoje a validade é uma só por produto.
- Curva ABC no dashboard entra no TCC (era "trabalho futuro" no texto)?
