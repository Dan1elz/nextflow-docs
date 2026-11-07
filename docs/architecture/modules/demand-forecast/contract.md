# Contrato — Inteligência de compras, painel e notificações

> **Status:** rascunho para validação · **Atualizado:** 2026-10-28 · Convenções: `../../contracts/README.md`
> Regras: `business-rules.md` (RN-DF*), `../catalog-inventory/business-rules.md` (RN-CE*) · DER: `../../diagrams/der-consolidado.md` (seção Previsão)
> Contrato anterior (versão em produção na `task-17`): `nextflow/docs/AI_FORECAST_SPEC.md` §7 — este documento o substitui quando implementado.

Princípio que guia cada tela: **o backend calcula, a IA interpreta, o humano decide** (decisão 0005). Todo número exibido vem
pronto da API; o texto da IA aparece sempre identificado ("motivo da IA" × "motivo calculado").

---

## T-DF1. Painel inicial (`/`)
Carrega em blocos independentes (falha de um bloco não derruba os outros):

| Bloco | Informações | Ação |
|--|--|--|
| KPIs de vendas | faturamento do mês, nº de vendas, ticket médio, comparação % com o mesmo mês do ano anterior (sazonal) e com o mês anterior | link para pedidos |
| Margem | margem bruta do mês (receita − custo médio dos itens vendidos, `order_items.unit_cost`) | — |
| Estoque baixo | nº de variações abaixo do mínimo no local (loja selecionada) + top 5 (produto, variação, local, disponível, mínimo) | link para produtos filtrados "estoque baixo" |
| Lotes vencendo | nº de lotes vencendo em 30 dias, valor a custo, top 5 (produto, lote, local, validade, quantidade) | link para T12 do catálogo |
| Recomendações | top 5 pendentes (Comprar, Promover, Transferir) por prioridade; data e status da última análise; badge "sem IA" | Comprar, Aplicar desconto, Transferir, Descartar, "Ver análise completa" |
| Próximos eventos | eventos do calendário nos próximos 90 dias com nº de produtos ligados e data em que a venda começa a subir (`nextDate − leadDays`) | link para a previsão filtrada pelo evento |
| Gráfico | vendas por mês dos últimos 12 meses × mesmos meses do ano anterior | — |

```ts
GET /api/dashboard/sales-kpis?storeId     → SalesKpisDto
GET /api/dashboard/low-stock?storeId      → LowStockSummaryDto
GET /api/dashboard/expiring-lots?storeId&days=30 → ExpiringLotsSummaryDto
GET /api/dashboard/upcoming-events?days=90 → UpcomingEventDto[]
GET /api/dashboard/sales-chart?storeId    → SalesChartDto
GET /api/forecasts/latest/top?limit=5     → ForecastTopDto

SalesKpisDto { month: string /* "2026-10" */; revenue; orderCount; averageTicket; grossMargin; grossMarginPercent;
  revenueVsLastYearPercent?: number; revenueVsLastMonthPercent?: number }
LowStockSummaryDto { count; items: { productId; productName; variantId; variantLabel; locationName; available; minQuantity }[] }
ExpiringLotsSummaryDto { count; totalCostValue; items: { productName; variantLabel; lotCode; locationName; expiresOn; daysToExpire; quantity }[] }
UpcomingEventDto { eventId; name; nextDate: DateOnly; demandStartsOn: DateOnly; productCount }
SalesChartDto { months: { month: string; revenue; revenueLastYear? }[] }
ForecastTopDto { run?: ForecastRunSummaryDto; recommendations: ForecastRecommendationListItemDto[] }   // run nulo = nunca rodou
```

## T-DF2. Previsão — página principal (`/forecast`)
**Cabeçalho** (`ForecastRunSummaryDto` da última análise): data/hora, origem (manual/agendada), horizonte em meses e período
(ex.: "nov/2026 a abr/2027", RN-DF17), status (Concluída / Concluída sem IA / Em andamento / Falhou), produtos analisados,
produtos enviados à IA, **progresso dos lotes** (ex.: "Lote 3 de 8", RN-DF20; lotes com falha destacados), duração, resumo da IA,
contagem por ação (Comprar, Promover, Transferir, Manter) e por status, próxima execução agendada (RN-DF18).

**Botão "Gerar nova análise"** (Admin): sem parâmetro de horizonte (é automático). Se já houver análise em andamento, o botão
fica desabilitado com o progresso. A geração é **assíncrona**: `POST` devolve o run em andamento; o front consulta o status a cada
5 s até concluir (ou recebe notificação) — **lacuna L-DF1**.

**Filtros:** ação, prioridade, status (Pendente, Aplicada, Descartada, Expirada), confiança, categoria (nível 1/2), fornecedor
preferido, classe ABC, evento do horizonte, "ajustada pela IA", busca por produto.
**Tabela** (`ForecastRecommendationListItemDto`, uma linha por produto): imagem, produto, categoria, classe ABC, ação, prioridade,
confiança, estoque atual (empresa), a chegar, cobertura em dias, demanda projetada no horizonte, quantidade sugerida
(com unidade), desconto sugerido (Promover), origem → destino (Transferir), **comprar até** (`deadline`), fornecedor preferido,
motivo (resumido; completo no detalhe), selo "IA ajustou", status.
**Ações por linha:** ver detalhe (T-DF3), Comprar (T-DF4), Aplicar desconto (T-DF6), Transferir (T-DF7), Descartar (T-DF8).
**Seleção múltipla:** "Comprar selecionados" (só linhas Comprar pendentes) → T-DF4 com vários produtos.

```ts
POST /api/forecasts/generate                      → ForecastRunSummaryDto (status Running)   // Admin; 409 se já há uma em andamento
GET  /api/forecasts/latest                        → ForecastRunSummaryDto | null
GET  /api/forecasts/{runId}/status                → ForecastRunProgressDto
GET  /api/forecasts/{runId}/recommendations?offset&limit&filters&sort&order → PaginationDto<ForecastRecommendationListItemDto>

ForecastRunSummaryDto { id; createdAt; trigger: ForecastTrigger; requestedByName?; horizonMonths; horizonStart: string; horizonEnd: string;
  status: ForecastRunStatus; aiModel?; summary?; errorMessage?; productsAnalyzed; productsSentToAi; durationMs?;
  batches: { total; completed; failed }; counts: { buy; promote; transfer; hold; pending; applied; dismissed; expired };
  nextScheduledAt?: string }
ForecastRunProgressDto { id; status; batches: { total; completed; failed }; percent: number }
ForecastRecommendationListItemDto { id; productId; productName; imageUrl?; categoryPath?; abcClass?: AbcClass;
  action: RecommendationAction; priority; confidence; status: RecommendationStatus;
  currentStock; incomingStock; coverageDays?; projectedDemand; saleUnit; decimalPlaces;
  suggestedQuantity?; suggestedDiscountPercent?; suggestedPromotionDays?;
  transfer?: { fromLocationName; toLocationName };
  deadline?: DateOnly; preferredSupplierId?; preferredSupplierName?;
  reasonShort: string; aiAdjusted: boolean; appliedLink?: { type: SourceType; id; number? } }
```

## T-DF3. Detalhe da recomendação / previsão do produto (drawer na `/forecast` e aba "Previsão" do produto = T-DF5)
Mesma visão nos dois lugares. Na aba do produto, mostra a recomendação pendente mais recente (se houver) e o histórico.

| Seção | Informações |
|--|--|
| Recomendação | ação, prioridade, confiança (com explicação: meses de histórico), status, motivo completo da IA e motivo calculado, o que a IA mudou (quantidade calculada × final, RN-DF12/22) |
| Números do cálculo | estoque atual, a chegar, reservado, cobertura, lead time efetivo (e de onde veio: média real ou cadastro), estoque de segurança, necessidade de compra, vida útil (se perecível) e limite por validade (RN-CE28), pedido mínimo e múltiplo (RN-CE27/30), cobertura alvo e classe ABC (RN-CE29), "projeção baseada no ano anterior" (RN-DF04) |
| Gráfico mensal | últimos 24 meses: vendido, vendido em promoção, dias sem estoque, demanda perdida, preço médio; projeção do horizonte; linha do estoque atual; marcadores de eventos |
| Sazonalidade | índice sazonal dos 12 meses (produto e categoria), meses de histórico |
| Eventos do horizonte | nome, data, início da subida (`leadDays`) — eventos ligados ao produto destacados |
| Rateio por variação | por variação: proporção histórica (%), quantidade sugerida, disponível por local (RN-DF21) |
| Precisão | últimas projeções × realizado (RN-DF19) |

```ts
GET /api/forecasts/recommendations/{id}                → ForecastRecommendationDetailDto
GET /api/forecasts/products/{productId}?months=24       → ProductForecastDto   // usado na aba do produto, sem recomendação obrigatória

ForecastRecommendationDetailDto = ForecastRecommendationListItemDto & {
  forecastRunId; reasonAi?: string; reasonCalculated: string;
  calculatedQuantity?: number; calculation: ForecastCalculationDto;
  variantSplit: VariantSplitDto[]; product: ProductForecastDto }
ForecastCalculationDto { leadTimeDays; leadTimeSource: "History" | "Supplier" | "ProductSupplier"; safetyStock; purchaseNeed;
  reservedStock; targetCoverageDays; shelfLifeDays?; maxByShelfLife?; minOrderQty?; orderMultiple?; basedOnLastYear: boolean;
  monthsOfHistory; maxDiscountPercent? }
ProductForecastDto { productId; productName; saleUnit; decimalPlaces;
  history: { month: string; quantitySold; quantitySoldOnPromo; daysOutOfStock; lostDemandQty; avgPrice?; revenue }[];
  projection: { month: string; projectedQuantity }[];
  seasonality: { month: number; productIndex?: number; categoryIndex?: number }[]; monthsOfHistory;
  events: { name; date: DateOnly; demandStartsOn: DateOnly; linkedToProduct: boolean }[];
  currentStock; accuracy: ForecastAccuracyItemDto[]; latestRecommendationId? }
VariantSplitDto { variantId; variantLabel; sharePercent; suggestedQuantity; availableByLocation: { locationName; available }[] }
```

## T-DF4. Aplicar "Comprar" (dialog)
Recebe 1 ou N recomendações Comprar. **Agrupa por fornecedor preferido** (sem preferido → seção "Escolha o fornecedor", combo
obrigatório). Para cada fornecedor: local de entrega (padrão: local de recebimento da loja selecionada), e por produto as
**linhas por variação** (rateio de T-DF3, editável), custo unitário (padrão: último custo do produto × fornecedor, editável),
total. Avisos não bloqueantes: quantidade abaixo do pedido mínimo, fora do múltiplo (oferece arredondar), acima do limite por validade.
Confirmar gera **um pedido de compra em Orçamento por fornecedor** (RN-DF15) e marca as recomendações como Aplicadas com link.
```ts
POST /api/forecasts/recommendations/purchase
ApplyPurchaseDto { groups: { supplierId; receiveLocationId; note?;
  items: { recommendationId; variantId; quantity; unitCost }[] }[] }
→ ApplyPurchaseResultDto { purchaseOrders: { id; number; supplierName; total }[]; recommendations: ForecastRecommendationListItemDto[] }
```

## T-DF5. Aba "Previsão" do produto
Ver T-DF3 (`GET /api/forecasts/products/{productId}`). Mostra também as promoções do produto (contrato de vendas).

## T-DF6. Aplicar "Promover" (dialog, Admin)
Carrega: preço atual, custo médio, desconto sugerido, dias sugeridos, máximo permitido (preserva margem, RN-DF08).
Campos: desconto %, início (padrão hoje), término (padrão hoje + dias − 1), escopo (todas as variações ou selecionadas).
Prévia: preço promocional por variação e margem. Abaixo do custo → aviso com confirmação (RN-VD13, `confirmWarnings`).
```ts
POST /api/forecasts/recommendations/{id}/promotion
ApplyPromotionDto { discountPercent; startDate: DateOnly; endDate: DateOnly; variantIds?: string[]; confirmWarnings?: boolean }
→ { promotionIds: string[]; recommendation: ForecastRecommendationListItemDto }
```

## T-DF7. Aplicar "Transferir" (dialog)
Carrega: origem, destino, por variação: disponível na origem, disponível e mínimo no destino, quantidade sugerida (editável).
Confirmar gera **transferência em Rascunho** já preenchida (RN-DF16) e abre T10 do catálogo para enviar.
```ts
POST /api/forecasts/recommendations/{id}/transfer
ApplyTransferDto { fromLocationId; toLocationId; items: { variantId; lotId?; quantity }[] }
→ { transferId; transferNumber; recommendation: ForecastRecommendationListItemDto }
```

## T-DF8. Descartar
Motivo opcional (lista: "Já comprei por fora", "Discordo da quantidade", "Produto vai sair de linha", Outro + texto).
```ts
POST /api/forecasts/recommendations/{id}/dismiss  { reasonCode?: DismissReason; note?: string }
```

## T-DF9. Histórico de análises (`/forecast/history`)
Lista: data, origem, horizonte, status, produtos analisados, enviados à IA, lotes com falha, contagem por ação, aplicadas/descartadas, duração.
Ação: abrir a análise (T-DF2 com aquele `runId`, só leitura se não for a mais recente). Filtros: período, status, origem.
```ts
GET /api/forecasts?offset&limit&filters → PaginationDto<ForecastRunSummaryDto>
GET /api/forecasts/{runId}               → ForecastRunSummaryDto
GET /api/forecasts/{runId}/batches       → { batchNumber; productsCount; status; errorMessage?; durationMs? }[]
```

## T-DF10. Precisão da previsão (`/forecast/accuracy`)
Visão geral: erro médio % por mês (últimos 12), por classe ABC e por categoria; % de produtos dentro de ±20%.
Tabela por produto: classe, meses medidos, erro médio %, último mês (previsto × vendido), tendência (subestima/superestima).
Usa só meses **completos** já encerrados (RN-DF19). Exclui meses com ruptura total? **Lacuna L-DF3**.
```ts
GET /api/forecasts/accuracy/summary?months=12 → ForecastAccuracySummaryDto
GET /api/forecasts/accuracy/products?offset&limit&filters → PaginationDto<ForecastAccuracyProductDto>
ForecastAccuracySummaryDto { monthly: { month; mapePercent; productsMeasured }[]; byAbcClass: { abcClass; mapePercent }[];
  byCategory: { categoryPath; mapePercent }[]; withinTolerancePercent }
ForecastAccuracyProductDto { productId; productName; abcClass?; monthsMeasured; mapePercent; bias: "Under" | "Over" | "Balanced";
  lastMonth?: { month; projected; actual } }
ForecastAccuracyItemDto { month; projected; actual; errorPercent }
```

## T-DF11. Agendamento (`/settings/forecast`)
Dia da semana e hora da análise automática (padrão segunda 06:00, fuso de negócio), ligado/desligado, tamanho do lote da IA
(padrão 40, RN-DF20), status da chave de IA (configurada ou não; nunca mostra a chave).
```ts
GET/PUT /api/settings/forecast  ForecastSettingsDto { scheduleEnabled; weekday: number; time: string /* "06:00" */; aiBatchSize; aiConfigured: boolean /* só leitura */ }
```

## T-DF12. Notificações (sino no topo, todas as telas)
Contador de não lidas; lista das últimas 20: ícone por tipo, título, texto curto, quando, link; marcar uma/todas como lidas.
Tipos: nova análise com recomendações (RN-DF18), lote vencendo, estoque baixo. Gerar notificação de estoque baixo a cada venda
viraria spam — **lacuna L-DF4**.
```ts
GET   /api/notifications?unreadOnly&limit=20 → { unreadCount: number; items: NotificationDto[] }
PATCH /api/notifications/{id}/read
PATCH /api/notifications/read-all
NotificationDto { id; type: NotificationType; title; message; link?; createdAt; readAt? }
```

---
## Enums (espelhar em `types/enums.ts`)
`RecommendationAction` Buy=1, Promote=2, Hold=3, **Transfer=4** · `RecommendationPriority` Low=1, Medium=2, High=3 ·
`ForecastConfidence` Low=1, Medium=2, High=3 · `RecommendationStatus` Pending=1, Applied=2, Dismissed=3, Expired=4 ·
`ForecastRunStatus` Completed=1, CompletedWithoutAi=2, Failed=3, **Running=4** · `ForecastTrigger` Manual=1, Scheduled=2 ·
`AiBatchStatus` Pending=1, Sent=2, Completed=3, Failed=4 · `AbcClass` A=1, B=2, C=3 ·
`DismissReason` BoughtElsewhere=1, DisagreeQuantity=2, WillDiscontinue=3, Other=4 ·
`NotificationType` NewRecommendations=1, LotExpiring=2, LowStock=3

## Lacunas encontradas neste módulo
- **L-DF1** Geração demorada (vários lotes de IA): recomendação — análise assíncrona em background (`Running`), progresso por polling de `/status` e notificação ao terminar; hoje o `POST generate` é síncrono.
- **L-DF2** Horizonte "maior lead time + 3, até 6" é da análise inteira; produtos de lead time curto recebem projeção longa sem necessidade. Recomendação: projeção sempre até o horizonte (útil no gráfico), mas a necessidade de compra usa o lead time de cada produto (como hoje).
- **L-DF3** Precisão em meses com ruptura: vender 0 por falta não é erro da previsão. Recomendação: excluir da média meses com > 50% dos dias sem estoque e sinalizar.
- **L-DF4** Notificações de estoque baixo e lote vencendo: recomendação — gerar 1 resumo diário (job), não por evento.
- **L-DF5** "Comprar" de produto com grade: rateio com variação sem histórico (tamanho novo). Recomendação: proporção igual entre as variações sem histórico, editável no dialog.
- **L-DF6** Recomendação Transferir é por local, mas a previsão é da empresa (RN-CE17). Recomendação: Transferir usa só saldo × mínimo/cobertura por local (sem previsão por local) até existir previsão por loja.
- **L-DF7** Recomendações pendentes de uma análise antiga quando uma nova está `Running`: recomendação — só expiram quando a nova conclui; se falhar, as antigas continuam valendo.
- **L-DF8** Quem é notificado: hoje só existe Admin; recomendação — notificar todos os usuários ativos (todos são Admin).
