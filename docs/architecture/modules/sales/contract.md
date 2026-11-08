# Contrato — Vendas

> **Status:** rascunho para validação · **Atualizado:** 2026-10-28 · Convenções: `../../contracts/README.md`
> Regras: `business-rules.md` (RN-VD*) · DER: `../../diagrams/der-consolidado.md` (seção Vendas)

Contexto global do front: **loja selecionada** no topo (`storeId`). Toda venda nasce nessa loja e baixa do local de venda
padrão dela (`stores.defaultSaleLocationId`), salvo escolha explícita de outro local vendável da mesma loja.
Estados de negócio (RN-VD16): **Orçamento** (com validade, reserva estoque) → **Pago**; ou Cancelado, Reembolsado, Expirado.

---

## T-VD1. Seletor de produto/variação para venda (componente usado em T-VD2 e T-VD4)
Campo único de busca que aceita **nome, SKU ou código de barras** (leitor = teclado + Enter). Código de barras exato adiciona
direto ao carrinho com quantidade 1; busca por nome abre lista.
**Cada opção mostra:** miniatura, nome do produto, rótulo da variação ("P / Azul"), SKU, preço de tabela, **preço efetivo**
(riscado o de tabela se há promoção, com "−X%"), **disponível no local de venda**, unidade (un, kg, m) e, se controla lote,
o lote que será baixado (FEFO, RN-CE15) e a validade dele.
Variações inativas ou de produto fora de linha **aparecem** (podem ser vendidas; RN-CE19 só bloqueia compra) — sinalizadas.
Disponível ≤ 0: opção marcada "sem estoque aqui"; se o produto não permite negativo (RN-CE32) não adiciona e mostra o aviso de falta (T-VD1a).

```ts
GET /api/sales/variant-options?search=&storeId=&locationId=&limit=20
VariantSaleOptionDto {
  variantId; productId; productName; variantLabel?: string;   // nulo = variação padrão oculta
  sku; barcode?; imageUrl?;
  saleUnit: SaleUnit; decimalPlaces: number; allowsNegative: boolean;
  listPrice: number; effectivePrice: number;
  activePromotion?: PromotionSummaryDto;      // vigente hoje (F2.3); nula sem promoção
  availableQuantity: number;                 // no local informado (físico − reservado)
  locationId: string;                        // local de venda resolvido (o informado ou o padrão da loja); o aviso de falta o exclui (F2.1)
  nextLot?: { lotId; code; expiresOn: DateOnly; quantity };   // só se tracksLots
  lifecycle: Lifecycle; isActive: boolean;
}
```

### T-VD1a. Aviso de falta
Quando a variação não tem disponível suficiente no local de venda, a API informa onde há saldo na empresa.
Ações: **Transferir agora** (cria transferência já Enviada+Recebida do local escolhido para o local de venda — só locais da
mesma loja; outra loja abre transferência em Rascunho, RN-CE12 e decisão (b) de lojas × locais), **Cliente procurou**
(registra demanda perdida, RN-CE24) ou cancelar.
```ts
GET /api/stock/availability?variantId=&excludeLocationId=
StockAvailabilityDto { variantId; byLocation: { locationId; locationName; storeId; storeName; sameStore: boolean; available }[] }
POST /api/stock-transfers/quick { fromLocationId; toLocationId; variantId; lotId?; quantity }   // mesma loja: envia e recebe na hora
POST /api/lost-demand { variantId; locationId; quantity }
```

## T-VD2. Venda rápida de balcão (`/sales/quick`)
Tela de uma coluna, otimizada para teclado (RN-VD15). Sem abertura/fechamento de caixa, TEF, cupom ou offline.
**Carrega:** loja e local de venda (do contexto), formas de pagamento disponíveis, cliente vazio.
**Carrinho, por linha:** nome + variação, quantidade (respeita casas decimais), preço efetivo unitário, desconto **R$ por item**
(RN-VD03; desconto ≤ preço × quantidade), total da linha, lote (só leitura) e remover.
**Rodapé:** subtotal (Σ preço efetivo × qtd), descontos (Σ descontos), **total**; cliente opcional (busca por nome/CPF ou
"Consumidor final"); pagamentos: uma ou mais linhas (forma + valor), mostra **falta pagar** e **troco** (troco só se houver
Dinheiro e o pago exceder o total; o valor gravado do pagamento em dinheiro é o líquido).
**Ação "Concluir":** cria o pedido já Pago (canal Counter) numa única chamada; a API revalida preço efetivo, disponível e
soma dos pagamentos = total (RN-VD05); baixa o estoque pelo `IStockLedger` (RN-CE14). Resposta: nº da venda e "Nova venda".
Se o preço mudou entre a busca e a conclusão: 422 com `errors.confirm` mostrando o novo total.

```ts
POST /api/sales/quick ← QuickSaleDto → 201 OrderDetailDto   // F2.4: OrderDetailDto ganha cashReceived? e change?
POST /api/sales/quick/preview ← QuickSaleDto → QuickSalePreviewDto   // F2.4: o rodapé vem da API, nada é gravado
QuickSaleDto {
  storeId; saleLocationId?;                 // nulo = padrão da loja
  clientId?;
  items: { variantId; quantity; discount: number; lotId?;   // lotId só se escolha manual (422 até a F1.7)
    expectedUnitPrice?: number }[];         // F2.4: effectivePrice mostrado; diferente do atual → 422 confirm
  payments: { method: PaymentMethod; amount: number }[];
  cashReceived?: number;                    // para calcular troco
  confirmWarnings?: boolean;
}
QuickSalePreviewDto { items: { variantId; listPrice; unitPrice; discount; lineTotal; promotion?: { id; discountPercent } }[];
  subtotal; discountTotal; total; paid; remaining; change? }   // remaining ≥ 0; change só com cashReceived e dinheiro
```
> **Ajustes de 08/11/2026 (em andamento na branch `feat/venda-rapida-ajustes`, sem push):**
> - **Leitor de código:** Enter com código exato adiciona direto (já era assim); quando não acha, a tela avisa e seleciona o termo
>   para a próxima leitura, e o Enter sem código exato **não** pega mais o 1º da lista. Com as setas, o Enter escolhe o destacado.
> - **Botão "Atualizar preços" removido:** a prévia (`/quick/preview`) já usa o preço atual, a linha avisa "Preço mudou" e o
>   `errors.confirm` ao concluir cobre a troca entre busca e conclusão. Substitui a decisão da F2.4 sobre o botão.
> - **Rodapé novo** (só front) e **e-mail opcional** no cadastro rápido de cliente (ver `purchasing/contract.md`, T-CD4).

## T-VD3. Pedidos — listagem (`/orders`)
**Carrega** (`OrderListItemDto`): nº, data de criação, canal (Balcão/Pedido), cliente (nome ou "Consumidor final"), loja,
vendedor (usuário), nº de itens, total, status com cor, validade (só orçamento; "vence em N dias"/"vencido"), data do pagamento.
**Filtros:** status (Orçamento, Pago, Cancelado, Reembolsado, Expirado), loja, canal, período (criação ou pagamento), cliente,
nº do pedido, produto (contém a variação). **Ordenação:** nº, data, total.
**Abas rápidas:** Orçamentos válidos · Pagos · Todos. **Ações:** novo orçamento (T-VD4), venda rápida (T-VD2), ver (T-VD5),
editar (só Orçamento).
Orçamento vencido aparece como **Expirado** sem job: status calculado na leitura (`validUntil < hoje`) e persistido na próxima escrita — **lacuna L-VD1**.

```ts
GET /api/orders?offset&limit&filters&sort&order&storeId
OrderListItemDto { id; number; createdAt; channel: OrderChannel; clientName?: string; storeName; userName;
  itemCount; total; status: OrderStatus; validUntil?: DateOnly; daysToExpire?: number; paidAt? }
```
> **Histórico de vendas (`/sales/history`, 08/11/2026, em andamento na branch `feat/historico-vendas`, sem push):** usa a mesma
> `GET /api/orders`, que passa a aceitar também `userId` (vendedor), `productId` (pedido com algum item do produto), `minTotal` e
> `maxTotal` (faixa de valor), além do cliente. Na tela, cada linha tem um botão único **Visualizar** (abre T-VD5) no lugar do menu
> de três pontos. Sem migration. Com a branch `feat/filtro-loja`, a busca refaz ao trocar a loja do topo e, em "Todas as lojas", a
> tabela mostra a coluna Loja.

## T-VD4. Orçamento — criar / editar (`/orders/create`, `/orders/:id/edit`)
Só existe edição enquanto **Orçamento** e não expirado (RN-VD04/16).
**Campos:** loja (contexto, só leitura na edição), local de venda (padrão da loja), cliente (opcional), validade (padrão
hoje + 7 dias, RN-VD14 — provisório; editável? **lacuna L-VD2**), itens (T-VD1; mesmas colunas do carrinho de T-VD2 +
coluna "disponível" já descontando a reserva deste orçamento), observação.
**Totais** iguais aos de T-VD2. Ao salvar, a reserva passa a valer (calculada, não gravada, RN-CE08).
Disponível insuficiente no momento de salvar: permitido salvar orçamento com aviso? **lacuna L-VD3** (recomendação: avisa
e salva; a reserva só cobre o que existe; o bloqueio acontece no pagamento).

```ts
GET  /api/orders/{id}/form → OrderFormDto
POST /api/orders           ← SaveOrderDto → OrderDetailDto
PUT  /api/orders/{id}      ← SaveOrderDto → OrderDetailDto
SaveOrderDto { storeId; saleLocationId?; clientId?; validUntil?: DateOnly; note?;
  items: { id?; variantId; quantity; discount: number }[]; version?: number; confirmWarnings?: boolean }
OrderFormDto = SaveOrderDto & { id; number; version; status;
  items: (SaveOrderDto['items'][number] & { productName; variantLabel?; sku; listPrice; effectivePrice; activePromotionPercent?; available; decimalPlaces })[];
  client?: { id; name; cpf? } }
```
> No orçamento o preço **não é congelado**: ao pagar vale o preço efetivo do dia (RN-VD02). Mostrar aviso "preços podem mudar
> até o pagamento"? **lacuna L-VD4** (recomendação: congelar o preço durante a validade é o comportamento esperado pelo cliente).

## T-VD5. Pedido — visualizar (`/orders/:id/view`)
**Cabeçalho:** nº, status, canal, loja, local de baixa, cliente (nome, CPF, link), vendedor, criado em, validade (orçamento),
pago em, cancelado/reembolsado em + motivo + por quem, observação.
**Itens:** produto, variação, SKU, quantidade + unidade, **preço de tabela** (`listPrice`), **preço cobrado** (`unitPrice`),
promoção aplicada (nome/percentual, link), desconto R$, total da linha, **lote baixado** (código + validade, após pagamento),
custo unitário e margem (só Admin — hoje todo usuário é Admin).
**Totais:** subtotal, descontos, total; **pagamentos:** forma, valor, data.
**Ações por status:**
| Status | Ações |
|--|--|
| Orçamento (válido) | Editar (T-VD4), **Pagar** (T-VD6), Cancelar (motivo obrigatório) |
| Expirado | Renovar validade? **lacuna L-VD1**, Duplicar como novo orçamento |
| Pago | **Reembolsar** (Admin, até 7 dias do pagamento, RN-VD08 — o "dias restantes" vem da API), sem cancelar (Pago só sai por reembolso) |
| Cancelado / Reembolsado | só leitura |
Reimprimir/comprovante: fora do escopo.

```ts
GET /api/orders/{id} → OrderDetailDto
OrderDetailDto { id; number; version; status: OrderStatus; channel: OrderChannel;
  store: { id; name }; saleLocation: { id; name }; client?: { id; name; cpf? }; user: { id; name };
  createdAt; validUntil?: DateOnly; paidAt?; canceledAt?; refundedAt?; statusReason?; statusChangedByName?; note?;
  items: { id; productId; productName; variantId; variantLabel?; sku; quantity; saleUnit; decimalPlaces;
    listPrice; unitPrice; discount; lineTotal; promotion?: { id; discountPercent }; lot?: { code; expiresOn };
    unitCost?; marginPercent? }[];
  subtotal; discountTotal; total;
  payments: { id; method: PaymentMethod; amount; createdAt }[];
  allowedActions: OrderAction[];          // a API decide; o front só mostra
  refundDeadline?: DateOnly }
POST /api/orders/{id}/cancel  { version; reason }
POST /api/orders/{id}/refund  { version; reason }       // devolve estoque ao local de baixa (RN-VD07)
```
> `allowedActions` evita o front recalcular regra de status/prazo (convenção do README).

## T-VD6. Checkout / pagamento de orçamento (drawer)
**Carrega:** resumo do pedido recalculado na hora (preço congelado do orçamento enquanto válido, RN-VD19; venda direta usa o preço efetivo do dia), total, disponível de
cada item no local de baixa (se faltar: aviso de falta T-VD1a por item).
**Campos:** pagamentos (forma + valor, múltiplos), dinheiro recebido (troco). Botão Confirmar habilita quando Σ = total.
**Efeito:** status → Pago, `paidAt`, baixa de estoque por item (lote FEFO), grava custo médio do momento em `order_items.unitCost`.
```ts
GET  /api/orders/{id}/checkout → CheckoutPreviewDto { orderId; version; total; items: { itemId; productName; variantLabel?; quantity; available; enough: boolean }[] }
POST /api/orders/{id}/pay ← { version; payments: { method; amount }[]; cashReceived?; confirmWarnings? } → OrderDetailDto
```

## T-VD7. Promoções (`/promotions`)
**Listagem** (`PromotionListItemDto`): produto, variação ("Todas" quando por produto), % de desconto, preço de tabela → preço
promocional (faixa se por produto), início, fim, **status calculado** (Agendada, Vigente, Encerrada, Cancelada), origem
(Manual / Recomendação da IA, com link), criada por, **abaixo do custo** (badge), vendas no período (qtd, opcional — **lacuna L-VD5**).
**Filtros:** status, origem, produto, período. **Ações:** nova promoção, cancelar (Agendada ou Vigente).

**Criar** (dialog): produto (busca), escopo (todas as variações ou uma variação), desconto % (1–90), início (≥ hoje), fim
(≥ início, máx. 90 dias inclusivos), motivo. **Prévia**: por variação, preço de tabela, preço promocional, custo médio e
margem resultante. Regras: sem sobreposição com outra promoção ativa da mesma variação (RN-VD11 adaptada à variação);
produto ativo; **abaixo do custo** → 422 `errors.confirm` e reenvio com `confirmWarnings: true`, gravando `belowCostConfirmed` (RN-VD13).
```ts
GET  /api/promotions?offset&limit&filters → PaginationDto<PromotionListItemDto>
PromotionListItemDto { id; productId; productName; variantId?; variantLabel?; discountPercent;
  minListPrice; maxListPrice; minPromoPrice; maxPromoPrice; startDate: DateOnly; endDate: DateOnly;
  status: PromotionStatus; source: PromotionSource; forecastRecommendationId?; reason?; createdByName; belowCostConfirmed: boolean; isActive }
// F2.3: filters = status, source, productId, from/to (período que cruza); início mais recente primeiro. POST devolve 201 com PromotionListItemDto.
// 422 por campo: discountPercent, startDate (antes de hoje ou sobreposição, L-VD10), endDate, productId (inexistente/inativo), variantId (de outro produto ou removida); confirm (RN-VD13).
// Preço promocional = tabela × (1 − %/100), 2 casas, meio para cima, só no IProductPricingService. Cancelar: 204; Encerrada ou Cancelada → 400.
GET  /api/promotions/preview?productId=&variantId=&discountPercent= → { variants: { variantId; variantLabel?; listPrice; promoPrice; averageCost?; marginPercent?; belowCost: boolean }[] }
POST /api/promotions ← { productId; variantId?; discountPercent; startDate; endDate; reason?; confirmWarnings? }
PUT  /api/promotions/{id}  PromotionRequestDto             // 200 PromotionListItemDto; só Agendada (400 nas demais);
                                                          // produto não muda (422 productId); mesmas regras da criação
                                                          // (RN-VD10, RN-VD11 sem contar ela mesma, RN-VD13). 08/11/2026
POST /api/promotions/{id}/cancel                         // 204; só Agendada ou Vigente
PromotionSummaryDto { id; discountPercent; endDate }     // usado em outras telas
```

---
## Enums (espelhar em `types/enums.ts`)
`OrderStatus` Budget=1, Paid=2, Canceled=3, Refunded=4, Expired=5 (**substitui** Budget/PendingPayment/PaymentConfirmed/Canceled/Refunded) ·
`OrderChannel` Counter=1, Order=2 · `PaymentMethod` Cash=1, CreditCard=2, DebitCard=3, BankTransfer=4, Pix=5 (boleto removido, RN-VD20) ·
`OrderAction` Edit=1, Pay=2, Cancel=3, Refund=4, Duplicate=5, Renew=6 ·
`PromotionStatus` Scheduled=1, Active=2, Ended=3, Canceled=4 (hoje é string calculada; vira enum numérico) · `PromotionSource` Manual=1, AiRecommendation=2

## Lacunas encontradas neste módulo
- **L-VD1** Orçamento expirado: renova a validade ou só duplica? E o status Expirado é gravado quando? Recomendação: status calculado na leitura, gravado em qualquer escrita; ação "Renovar" (+7 dias) além de "Duplicar".
- **L-VD2** Validade editável por orçamento ou fixa em 7 dias? Recomendação: padrão 7, editável de 1 a 30.
- **L-VD3** Salvar orçamento sem estoque disponível: recomendação avisar e permitir; bloqueio só no pagamento.
- **L-VD4** Preço do orçamento congela até a validade ou segue o preço efetivo do dia? Hoje segue o do dia (RN-VD02). Recomendação: **congelar** durante a validade (o cliente espera pagar o orçado); exige gravar `listPrice/unitPrice` no orçamento.
- **L-VD5** Mostrar vendas durante a promoção na listagem? Recomendação: sim (qtd vendida no período), barato de calcular e útil para avaliar a IA.
- **L-VD6** Boleto (`Ticket`) existe hoje; com RN-VD18 (sem prazo) sai? Recomendação: remover.
- **L-VD7** Cancelar pedido Pago (hoje existe, devolve estoque) × reembolso: recomendação — Pago só sai por Reembolso (um caminho, RN-VD08); Cancelar só para Orçamento.
- **L-VD8** Prazo de 7 dias do reembolso conta de `paidAt` (o código atual conta da última atualização). Recomendação: `paidAt`.
- **L-VD9** Reembolso parcial (um item) segue fora? Recomendação: fora (reembolso total + nova venda).
- **L-VD10** ~~Promoção por variação muda RN-VD11 (sobreposição): promoção do produto inteiro e outra de uma variação no mesmo período conflitam?~~ **Fechada na F2.3 pela recomendação:** conflitam; duas variações diferentes no mesmo período, não.
