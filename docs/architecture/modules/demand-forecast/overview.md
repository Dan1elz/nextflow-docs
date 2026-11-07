# Módulo Inteligência de compras — visão

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** `nextflow/docs/AI_FORECAST_SPEC.md` (contrato), `PROJECT.md` §5.1.1, TCC (RF003, quadro 6)

## O que faz hoje
O Admin gera uma análise (horizonte de 1 a 3 meses). O sistema agrega as vendas confirmadas dos últimos 36 meses, calcula
índice sazonal, demanda projetada, cobertura e necessidade de compra ou promoção, envia o resultado à IA (Gemini) para
priorizar e explicar, aplica guardrails e grava a análise. Cada produto recebe **Comprar**, **Promover** ou **Manter**,
com prioridade, confiança e motivo. O Admin aplica (gera pedido de compra ou promoção) ou descarta.
É o **diferencial do produto** (decisão global 0001) e segue a decisão 0005 (backend calcula, IA interpreta, humano decide).

## Onde aparece
Card "Recomendações da IA" no dashboard, página `/forecast`, aba "Previsão" do produto e página de promoções.

## Contrato técnico
`../../../../../nextflow/docs/AI_FORECAST_SPEC.md` (fonte do contrato back↔front). Integração: `../../integrations/gemini.md`.

## Problemas conhecidos (a validar)
- Itens de temporada zerados aparecem como "Comprar alta" (bug do motor apontado na thread de storage, 27/10/2026).

## Perguntas em aberto
- A análise deve rodar sozinha (agendada) ou continuar sob demanda?
- Usa estoque físico ou disponível (com a reserva nova)?
- Horizonte de 1 a 3 meses atende o público? Datas comerciais além das nacionais (ex.: festas locais)?
