# Bloco C: o que falta, em fatias mínimas

> **Escrito em 08/11/2026**, depois da review de F3.1 a F3.5 e F3.7 (back `d27ae54`, 969/969 testes verdes, branch local
> `feat/bloco-c-previsao`, sem push). Cada fatia é pequena, tem aceite e testes **definidos antes do código** (TDD) e vira um cartão
> `F*.md` próprio quando começar. Ordem sugerida de cima para baixo dentro de cada grupo; o front pode correr em paralelo ao back da F3.6.
> Ao aprovar o bloco, **tudo vai para a `homolog`** (back e front) e a branch de docs entra na `main` dos docs.

## Back

| Fatia | Entrega mínima | Aceite | Testes |
|--|--|--|--|
| **F3.6a** Precisão: cálculo puro | `ForecastAccuracyCalculator` (erro % do mês, MAPE e viés do produto, ±15% (era ±20% até 08/11, `b852dfc`), ruptura > 50% e vendido zero fora) | ver `F3.6a.md` | 11 unitários (`ForecastAccuracyCalculatorTests`) |
| **F3.6b** Precisão: projeção de referência (feita, `9bd4812`, `F3.6b.md`) | Consulta no repositório: por produto e mês **completo**, a projeção da última análise concluída com `referenceDate` antes do 1º dia do mês, junto com `product_sales_monthly` (vendido e dias sem estoque) | Mês sem análise anterior não aparece; análise `Failed` é ignorada; mês corrente não entra (RN-DF19) | Integração `ForecastAccuracyQueryTests`: 3 casos acima com 2 análises montadas à mão |
| **F3.6c** Precisão: rotas (feita, `a8ee2e2`, `F3.6c.md`) | `GET /api/forecasts/accuracy/summary?months=12` e `GET /api/forecasts/accuracy/products` (T-DF10) e `accuracy` preenchido em `GET /api/forecasts/products/{id}` (T-DF5) | Resumo por mês, classe ABC e categoria; tabela paginada com viés e último mês; só Admin | Integração em `ForecastApiTests`: resumo, lista paginada, 403 para não Admin, `accuracy` no T-DF5 |
| **F3.4c** 422 do Aplicar Comprar por fornecedor (feita, `a106162`, `F3.4c.md`) | `PurchaseOrderRules.Check` roda uma vez por grupo (fornecedor) sobre os itens **somados por variação**, então o índice `groups[i].items[k]` do erro é o da lista somada, não o da linha enviada. Mapear o erro de volta para a(s) linha(s) originais | Fornecedor inativo no 2º grupo → 422 em `groups[1].supplierId`; variação inativa repetida em duas linhas → 422 nas duas linhas certas; nada gravado | Integração em `ForecastActionsTests` (2 casos) |
| **F3.4b** ✂ Transferir (opcional) | Fatiar ao começar: (1) gatilho puro de excesso × falta entre locais (RN-DF16); (2) motor e IA com a ação `Transfer`; (3) aplicar gera transferência | A definir no cartão | A definir no cartão |

## Front (telas T-DF; build e lint, a conferência visual é do Daniel)

| Fatia | Entrega mínima | Aceite |
|--|--|--|
| **F3.8a** Enums e tipos (feita, front `d3ee3b6`, branch `feat/bloco-c-front`) | `TLeadTimeSource` (History=1, ProductSupplier=2, Supplier=3) e os tipos dos DTOs da previsão em `src/types` | Build e lint limpos; nomes iguais ao back (enums trafegam pelo nome) |
| **F3.8b** Painel inicial | Trocar `/api/dashboard/stats` (não existe) pelas rotas de T-DF1 e `forecasts/latest/top` | Painel carrega sem 404 com o seed |
| **F3.8c** Sino | T-DF12: contador, lista das 20 últimas, marcar uma/todas | Marca como lida e o contador cai |
| **F3.8d** Lista da análise | `/forecast` (T-DF2): última análise, filtros, botão gerar com progresso e 409 tratado | Gerar mostra "Em andamento" e recarrega ao terminar |
| **F3.8e** Detalhe | Drawer T-DF3 e aba Previsão do produto (T-DF5) | Rateio soma a quantidade sugerida |
| **F3.8f** Comprar | Dialog T-DF4 (um ou vários produtos, grupos por fornecedor, avisos não bloqueiam) | Gera pedido em Orçamento e a linha vira Aplicada |
| **F3.8g** Promover e Descartar | T-DF6 e T-DF8 | Descartar "Outro" sem texto mostra o erro no campo |
| **F3.8h** Histórico e agendamento | T-DF9 e T-DF11 | Salvar o agendamento mostra a próxima execução |
| **F3.8i** Precisão | T-DF10, depois da F3.6c | Gráfico por mês e tabela por produto |

## Fecha o bloco
- QA do bloco C pelo Daniel (RN-DF24, RN-DF25 e RN-DF26 aprovadas em 08/11; demais decisões abertas nos cartões F3.1 a F3.5).
- Merge na `homolog`: back `feat/bloco-c-previsao`, front (enums + telas) e docs `docs/bloco-c-previsao` → `main`. Push só quando o Daniel pedir.
