# Contrato — Catálogo e estoque

> **Status:** rascunho para validação · **Atualizado:** 2026-10-31 · Convenções: `../../contracts/README.md`
> Regras: `business-rules.md` (RN-CE*) · DER: `../../diagrams/der-catalogo-v2-sazonalidade.md`, `der-catalogo-estoque.md`

Contexto global do front: **loja selecionada** no topo (`storeId`, padrão = última usada; "Todas" para o Admin).
Telas de estoque usam esse `storeId` como filtro padrão. Empresa com 1 loja e 1 local não vê seletor nem colunas de local (RN-CE12).

---

## T1. Produtos — listagem (`/products`)
**Carrega** (`ProductListItemDto`, uma linha por produto, não por variação):
imagem (miniatura), nome, marca, tipo de produto, categoria principal (RN-CE52), nº de variações ativas ("Sem grade" quando `hasVariants` é falso), faixa de preço
(menor–maior preço efetivo das variações ativas), ciclo de vida, ativo.

**Filtros (F1.3):** busca (nome, marca, SKU, código de barras de qualquer variação), categoria (nível 1 traz as filhas), tipo, coleção, ciclo de vida, ativo.
**Ordenação (F1.3):** nome, preço (menor preço entre as variações ativas).
**Ações:** novo produto (T2), ver (T3), editar (T2), inativar/reativar, marcar fora de linha.

**Provisório até a fatia dona, sem campo morto na tela:**
| O quê | Valor hoje | Entra em |
|--|--|--|
| `hasLowStock`, filtro "só estoque baixo" | F1.8: real; filtro `lowStock=true` | entregue |
| ordenação por disponível | F1.8: `sort=available`, mesmo recorte do disponível | entregue |
| `activePromotionPercent` e badge | F2.3: maior desconto vigente entre as variações não removidas; badge "−X%" no preço | entregue |
| filtro "em promoção" e ordenação por preço efetivo | fora; `sort=price` segue o preço de tabela | depois do bloco C |
| `min/maxEffectivePrice` | preço efetivo com a promoção vigente, por `IProductPricingService` | entregue (F2.3) |

```ts
GET /api/products?offset&limit&filters&sort&order
// filters: search, categoryId, productType, collectionId, lifecycle, isActive, storeId. sort: name, price
// storeId (F1.5) não filtra produto: só escolhe a loja do disponível; sem ele, a empresa inteira
ProductListItemDto {
  id; name; brand?: string; imageUrl?: string;
  productType: ProductType; lifecycle: Lifecycle; isActive: boolean;
  categoryPath?: string;               // "Doces › Chocolates"
  hasVariants: boolean; variantCount: number;
  minEffectivePrice: number; maxEffectivePrice: number;
  activePromotionPercent?: number;     // F2.3: maior desconto vigente; nulo sem promoção
  availableQuantity: number;           // F1.5: físico em locais ativos da loja do filtro (ou empresa); sem orçamento, disponível = físico (RN-CE08)
  saleUnit: SaleUnit; decimalPlaces: number;
  hasLowStock: boolean;                // F1.8: alguma variação ativa, em algum local ativo do recorte, com disponível < mínimo efetivo (RN-CE33)
}
PATCH  /api/products/{id}/lifecycle  { lifecycle: Lifecycle } → 204   // RN-CE19; inativo: 400 (RN-CE04)
DELETE /api/products/{id}            → 204   // inativa
PATCH  /api/products/{id}/reactivate → 204
```
> O contrato trazia `PATCH /{id}/active { isActive }`. A ADR 0010, mais recente, fixa `DELETE /{id}` e `PATCH /{id}/reactivate` para todo recurso; seguida a ADR.

## T2. Produto — criar / editar (`/products/create`, `/products/:id/edit`)
O formulário mostra e abre campos conforme o **tipo** (RN-CE20, RN-CE55):
| Seção | Campos | Aparece para | Fatia |
|--|--|--|--|
| Básico | nome, marca, tipo, categorias (multi, 2 níveis), imagem, descrição | todos | F1.3 |
| Venda | unidade de venda, casas decimais (preenchida pela unidade), permite negativo (RN-CE32) | todos | F1.3 |
| Grade | tem variações? atributos (Tamanho, Cor) e valores; botão "gerar combinações" | Vestuário (ligada, com Tamanho P/M/G), opcional nos demais | F1.3 |
| Variações | tabela: combinação, SKU, código de barras, preço, ativo | sempre (sem grade = 1 linha, sem combinação nem ativo) | F1.3 |
| Validade | controla lote, vida útil (dias) | Perecível (padrão ligado), opcional nos demais | F1.3 |
| Sazonalidade | coleção, data de lançamento | todos (coleção destacada no Vestuário) | F1.3 |
| Sazonalidade | eventos que puxam a venda (tags) | todos | F1.4 |
| Estoque | mínimo padrão do produto; mínimos por local (tabela local × mínimo) (RN-CE33); cobertura alvo (vazio = classe ABC) | todos | F1.8 |
| Fornecedores | tabela: fornecedor, preferido, código no fornecedor, prazo, pedido mínimo, múltiplo (RN-CE27, RN-CE30) | todos | F1.4 |

Custo **não é digitado** (vem das compras, RN-CE31). Na criação, saldo inicial é lançado depois por ajuste "Saldo de abertura" (T9).
Editar o preço de uma variação grava `price_history` (RN-CE25, RN-CE59).
A tela sugere o SKU das combinações novas (`NOME-VALOR`), editável; sem nome preenchido não sugere, e o botão preenche depois. "Gerar combinações" mantém as linhas existentes: primeiro a de combinação igual, depois a que cabe na combinação nova e, por fim, a que contém a combinação (quando um atributo sai).
A imagem sobe depois de salvar o produto, em chamada própria. Se falhar, o produto fica gravado e a tela avisa.

**Validações:** nome obrigatório; ≥ 1 variação, ≥ 1 ativa (RN-CE54); sem grade, exatamente 1 (RN-CE48); grade conforme RN-CE49; `tempKey` conforme RN-CE50; SKU e código de barras únicos (RN-CE57); preço > 0, até 2 casas;
casas decimais 0–3; vida útil > 0 obrigatória quando controla lote (RN-CE56); categoria e coleção novas precisam estar ativas (RN-CE53); eventos novos precisam estar ativos (RN-CE61); fornecedor sem repetir, no máximo um preferido, fornecedor novo ativo, `minOrderQty` e `orderMultiple` inteiros > 0 (RN-CE60).
Remover variação: não apaga, fica gravada como removida e sai do formulário (RN-CE58); o SKU e o código de barras dela ficam reservados para sempre (RN-CE57). Atributo e valor que saem são apagados (RN-CE51). Variação com saldo ≠ 0 não sai: 422 em `variants` (F1.5). Movimentação antiga não impede, porque a removida continua gravada.

```ts
GET  /api/products/form           → ProductFormDto   // criação: só options
GET  /api/products/{id}/form      → ProductFormDto   // tudo que o formulário precisa, de uma vez
POST /api/products                ← ProductRequestDto → 201 ProductResponseDto
PUT  /api/products/{id}           ← ProductRequestDto → ProductResponseDto
POST /api/products/{id}/image     (multipart, campo image) → { imageUrl }   // RN-CE05; erro em fieldErrors.image
DELETE /api/products/{id}/image   → 204

ProductRequestDto {
  name; brand?; description?; productType: ProductType; categoryIds: string[];
  saleUnit: SaleUnit; decimalPlaces: number; allowsNegative: boolean;
  tracksLots: boolean; shelfLifeDays?: number;
  collectionId?: string; launchedOn?: DateOnly;
  attributes: { id?: string; name: string; values: { id?: string; tempKey?: string; value: string }[] }[];
  variants: { id?: string; attributeValueIds: string[] /* id ou tempKey */; sku: string; barcode?: string; price: number; isActive: boolean }[];
  eventIds: string[];   // RN-CE61
  suppliers: { supplierId: string; isPreferred: boolean; supplierSku?: string; leadTimeDays?: number /* vazio = do fornecedor */; minOrderQty?: number; orderMultiple?: number }[];   // RN-CE60
}
ProductFormDto = ProductRequestDto & { id?; imageUrl?; options: ProductFormOptionsDto }
ProductFormOptionsDto { categories: CategoryOptionDto[]; collections: Option[]; events: Option[]; suppliers: SupplierOptionDto[] }   // ativos + os já vinculados
SupplierOptionDto { id; name; leadTimeDays /* padrão do campo vazio */; isActive /* marca o inativo já vinculado */ }
// Variações removidas (RN-CE58) não vêm no formulário.
// F1.8 no ProductRequestDto: defaultMinQuantity (≥ 0, até 3 casas); targetCoverageDays? (1–365; vazio = classe ABC);
// locationMinimums: { variantIndex /* posição em variants */; locationId; minQuantity /* ≥ 0 */ }[] — substitui a tabela inteira.
// variantIndex fora de variants ou variação × local repetido → 422; local fechado (salvo o já gravado) → 422.
// ProductFormDto devolve os três campos e options.locations (LocationOptionDto[]: ativos de loja ativa + os que já têm mínimo).
```
> Atributos/valores novos chegam sem `id`; a API cria. Para referenciar valor novo numa variação ainda sem id, o front usa `tempKey` (string) em `values` e em `attributeValueIds` (L1, RN-CE50).

## T3. Produto — visualizar (`/products/:id/view`)
Cabeçalho (`ProductResponseDto`), na F1.3: imagem, nome, marca, tipo, categorias, coleção, ciclo de vida, unidade, preço efetivo (faixa), lançamento, lote e validade, estoque negativo; eventos (F1.4).
F1.5: custo médio em faixa (entre as variações ativas com custo) e disponível (físico da empresa inteira, somado entre as variações). Entram depois: classe ABC e cobertura alvo efetiva (F1.8, fora do DTO); promoção vigente (F2.3, entregue).
Abas (cada uma carrega sob demanda). Só aparecem as que têm dado: **a partir da F1.4, Variações, Fornecedores e Preços**.

| Aba | Carrega | Ações | Fatia |
|--|--|--|--|
| Variações | por variação, sem as removidas (RN-CE58): combinação ("Padrão" sem grade), SKU, código de barras, preço, preço efetivo, status. F1.5: custo médio, último custo, margem % ((preço efetivo − médio) / preço efetivo) e disponível da empresa. Depois: promoção (F2.3) | editar (T2) | F1.3 |
| Estoque | matriz variação × local (variações ativas × locais ativos de lojas ativas, da loja selecionada ou todas): físico, reservado (0 até haver orçamento), disponível, mínimo e abaixo do mínimo (F1.8) | ajuste/perda (T9, F1.6), transferir (T10), "cliente procurou" (T14) | F1.5 em diante |
| Lotes | por lote com saldo ≠ 0: código, variação, loja/local, validade, dias para vencer (dia de negócio), selo vencido / vence em até 30 dias (janela fixa `LotAlert.ExpiringSoonDays`, **não confirmada pelo Daniel**), quantidade; ordem FEFO; a aba só aparece em produto que controla lote (`tracksLots`) e segue a loja do topo (`storeId`), como a matriz | — | F1.7 |
| Movimentações | kardex do produto (T8 filtrado) | — | F1.8 |
| Fornecedores | fornecedor, preferido, prazo, mínimo, múltiplo, último custo, última compra | — | F1.4 |
| Preços | histórico: variação (inclui as removidas, marcadas, RN-CE58), SKU, preço, de, até, quem alterou; mais recente primeiro (RN-CE59) | — | F1.4 |
| Previsão | ver contrato de demand-forecast (T-DF5) | — | Fase 3 |
| Promoções | ver contrato de vendas (T-VD7) filtrado | criar promoção | F2.3 |

```ts
GET /api/products/{id}                         → ProductResponseDto
GET /api/products/{id}/variants                → ProductVariantResponseDto[]   // sem as removidas
GET /api/products/{id}/price-history           → PriceHistoryDto[]             // F1.4
GET /api/products/{id}/suppliers               → ProductSupplierDto[]          // F1.4, preferido primeiro
GET /api/products/{id}/stock?storeId           → StockMatrixDto                // F1.5; sem storeId, todas as lojas ativas
// F1.8: StockMatrixCellDto.minQuantity = mínimo efetivo (o do local ou o padrão do produto); isBelowMin = available < minQuantity
// F1.7 (a loja do topo, como a matriz):
GET /api/products/{id}/lots?storeId            → LotBalanceDto[]   // { lotId; code; expiresOn; daysToExpire; isExpired; isExpiringSoon; variantId; variantLabel; locationId; locationName; storeName; quantity }

ProductResponseDto { id; name; brand?; description?; imageUrl?; productType; lifecycle; isActive; launchedOn?;
  categories: CategoryOptionDto[]; collection?: Option; saleUnit; decimalPlaces; allowsNegative;
  tracksLots; shelfLifeDays?; hasVariants;
  minAverageCost?; maxAverageCost? /* nulos sem entrada com custo */; minEffectivePrice; maxEffectivePrice; activePromotionPercent? /* F2.3: maior desconto vigente */;
  availableQuantity: number /* físico da empresa inteira */; variantCount /* ativas */; events: Option[] /* F1.4 */ }
// Entram depois: abcClass, targetCoverageDays, targetCoverageFromClass (F1.8)
ProductVariantResponseDto { id; label: string /* "P / Azul"; vazio na variação oculta */; sku; barcode?; price; effectivePrice;
  averageCost?; lastCost?; marginPercent? /* nulos sem entrada com custo */; availableQuantity: number /* físico da empresa */; isActive }
// F2.3: ProductVariantResponseDto.activePromotion?: PromotionSummaryDto (vigente hoje)
StockMatrixDto { locations: { id; name; storeName }[]; rows: { variantId; variantLabel; sku;
  cells: { locationId; physical; reserved /* 0 até F2.x */; available; minQuantity? /* nulo até F1.8 */; isBelowMin: boolean /* falso até F1.8 */ }[] }[] }
LotBalanceDto { lotId; code; expiresOn: DateOnly; daysToExpire: number /* negativo = vencido */; isExpired: boolean;
  isExpiringSoon: boolean /* 0 ≤ dias ≤ 30, janela fixa não confirmada */; variantId; variantLabel; locationId; locationName; storeName; quantity }
PriceHistoryDto { id; variantLabel /* vazio na oculta */; sku; variantRemoved; price; validFrom: DateOnly; validTo?: DateOnly; changedByName }  // variação removida do formulário fica gravada (inativa, RemovedOn) e continua no histórico
ProductSupplierDto { supplierId; supplierName; supplierIsActive; isPreferred; supplierSku?; leadTimeDays: number /* efetivo */; minOrderQty?; orderMultiple?; lastCost?; lastPurchaseOn?: DateOnly }
```

## T4. Categorias (`/categories`)
Lista em árvore: nível 1 com filhos; nº de produtos; ativo. Criar e editar em dialog, sem rota própria. Form: nome, descrição, categoria pai (só nível 1 pode ser pai, RN-CE23; o combo só traz o nível 1 e fica travado em categoria que tem filhas).
Não inativa categoria com produtos ativos sem confirmar (RN-CE53): 422 com `fieldErrors.confirm`, e o front reenvia confirmando. `productCount` conta os produtos ativos vinculados direto à categoria. Regras de RN-CE38 e RN-CE39.
```ts
GET /api/categories/tree → CategoryNodeDto[]  { id; name; description?; parentId?; isActive; productCount; children: CategoryNodeDto[] }
GET /api/categories/options?search=&filters={"rootsOnly":"true"} → CategoryOptionDto[]  { id; name; parentId?; path }   // só ativas; path = "Pai > Filha"
GET /api/categories/{id} → CategoryResponseDto  { id; name; description?; parentId?; isActive }
POST/PUT /api/categories  CategoryRequestDto { name; description?; parentId? } → CategoryResponseDto   // neta: 422 em fieldErrors.parentId
DELETE /api/categories/{id}?confirmWarnings=  // inativa; com subcategoria ativa: 400; com produto ativo e sem confirmar: 422 em fieldErrors.confirm (RN-CE53)
PATCH  /api/categories/{id}/reactivate        // subcategoria de pai inativo: 400
```

## T5. Coleções (`/collections`)
Lista: nome, início, fim, nº de produtos, status; busca por nome e filtro de status. Criar e editar em dialog. Form: nome, início e fim opcionais (fim ≥ início, RN-CE40).
`productCount` conta os produtos ativos da coleção (RN-CE53).
```ts
GET /api/collections → PaginationDto<CollectionResponseDto>  { id; name; startsOn?; endsOn?; productCount; isActive }
GET /api/collections/options?search= → Option[]   // só ativas
GET /api/collections/{id} → CollectionResponseDto
POST/PUT /api/collections  CollectionRequestDto { name; startsOn?; endsOn? } → CollectionResponseDto
DELETE /api/collections/{id}                  // inativa
PATCH  /api/collections/{id}/reactivate
```

## T6. Calendário de eventos (`/calendar-events`)
Lista: nome, escopo (Nacional/Da empresa), regra de data, **próxima data calculada**, antecedência (dias), nº de produtos, ativo; busca por nome e filtros de status e escopo, em ordem de nome. Criar e editar em dialog.
Nacionais vêm do seed e só podem ter a antecedência alterada e ser desativados; os da empresa são CRUD completo (RN-CE22), em que excluir é inativar, nos dois escopos (RN-CE43).
`scope` não vem do cliente: POST sempre cria `Company` (RN-CE42). `nextDate` é calculado só na API (RN-CE46). `productCount` conta só os produtos ativos vinculados (RN-CE61).
Campos por regra (RN-CE41), e os de fora são gravados como nulo: `Fixed` = `month` + `day` (sem 29/02); `NthWeekday` = `month` + `nthWeekday.weekday` (0 = domingo a 6 = sábado) + `nthWeekday.nth` (1 a 4); `EasterOffset` = `easterOffsetDays` (-60 a 60); `Easter` e `BlackFriday` = nenhum. `leadDays` obrigatório, de 0 a 120 (RN-CE45).
```ts
GET /api/calendar-events?filters={"search":"","isActive":"true","scope":"National"} → PaginationDto<CalendarEventResponseDto>
CalendarEventResponseDto { id; name; scope: EventScope; dateRule: DateRule; month?; day?; nthWeekday?: { weekday; nth }; easterOffsetDays?; leadDays; nextDate: DateOnly; productCount; isActive }
GET /api/calendar-events/options?search= → Option[]   // só ativos
GET /api/calendar-events/{id} → CalendarEventResponseDto
POST/PUT /api/calendar-events  CalendarEventRequestDto { name; dateRule; month?; day?; nthWeekday?: { weekday; nth }; easterOffsetDays?; leadDays } → CalendarEventResponseDto
// nome repetido: 422 em fieldErrors.name (RN-CE44). PUT de nacional com nome ou regra diferentes: 400 (RN-CE42)
DELETE /api/calendar-events/{id}                  // inativa
PATCH  /api/calendar-events/{id}/reactivate
```

## T7. Lojas e locais (`/settings/stores`)
Lista de lojas com seus locais (nome, vendável, ativo) e, por loja, local padrão de venda e de recebimento. Criar e editar loja e local, inativar e reativar.
Criar loja já cria o local "Loja", vendável, como padrão de venda e de recebimento, no mesmo commit (RN-CE35).
Regras: toda loja tem ≥ 1 local ativo; local padrão de venda precisa ser vendável; padrões são locais ativos da própria loja; não inativa local padrão (decisão 7).
Não inativa local com saldo ≠ 0 (RN-CE35) nem loja com saldo ≠ 0 em algum local (RN-CE36): 422. `hasStock` diz se o local tem saldo ≠ 0 (F1.5).
Inativar loja: última loja ativa não sai; os locais ficam como estão, mas saem dos combos; loja inativa não recebe nem altera locais (RN-CE36).
Seletor do topo: lojas de `CurrentUserDto.stores` (só ativas), última usada no `localStorage` (decisão 1). Com mais de uma loja há "Todas as lojas". Empresa com 1 loja e 1 local ativo não vê seletor (RN-CE12).
```ts
GET    /api/stores?offset&limit&filters → PaginationDto<StoreResponseDto>   // filters: search, isActive
GET    /api/stores/{id} → StoreResponseDto
POST   /api/stores      StoreRequestDto → 201 StoreResponseDto
PUT    /api/stores/{id} UpdateStoreRequestDto → StoreResponseDto
DELETE /api/stores/{id}             → 204   // inativa
PATCH  /api/stores/{id}/reactivate  → 204
GET    /api/stores/options?search   → Option[]   // só ativas, até 20

POST   /api/stock-locations      LocationRequestDto → 201 LocationResponseDto
PUT    /api/stock-locations/{id} UpdateLocationRequestDto → LocationResponseDto
DELETE /api/stock-locations/{id}            → 204   // inativa
PATCH  /api/stock-locations/{id}/reactivate → 204
GET    /api/stock-locations/options?search&filters → LocationOptionDto[]   // só ativos de loja ativa, até 20; filters: storeId, isSellable

StoreRequestDto { name }
UpdateStoreRequestDto { name; defaultSaleLocationId; defaultReceiveLocationId }
StoreResponseDto { id; name; isActive; defaultSaleLocationId?; defaultReceiveLocationId?; locations: LocationResponseDto[] }
UpdateLocationRequestDto { name; isSellable = true }
LocationRequestDto extends UpdateLocationRequestDto { storeId }
LocationResponseDto { id; storeId; name; isSellable; isActive; hasStock: boolean /* saldo ≠ 0 no local */ }
LocationOptionDto { id; name; storeId; storeName; isSellable }
```

## T8. Movimentações / kardex (`/stock-movements`)
**Carrega** (`StockMovementListItemDto`): data/hora, produto + variação, local, lote, tipo (entrada/saída), motivo, quantidade
com sinal, custo unitário, **saldo após** (saldo da chave variação × local × lote: com lote, é o saldo do lote no local, F1.7; a coluna Lote avisa), origem com link (pedido nº, compra nº, transferência nº, inventário nº), usuário, observação.
**Filtros:** período, loja/local, produto/variação, motivo, origem. **Ações:** novo ajuste/perda (T9). Sem editar nem excluir (RN-CE14).
```ts
GET /api/stock-movements?offset&limit&filters → PaginationDto<StockMovementListItemDto>   // F1.8; mais recente primeiro
// filters: from, to (yyyy-MM-dd, dia de negócio; "to" inclui o dia), storeId, locationId, productId, variantId, reason, sourceType
// source é nulo no lançamento manual (sem documento); lotCode nulo em produto sem lote (F1.7); number nulo até cada documento existir
```
```ts
StockMovementListItemDto { id; createdAt; productId; productName; variantId; variantLabel; locationId; locationName; lotCode?;
  type: MovementType /* In, Out */; reason: MovementReason; quantity /* com sinal */; unitCost?; balanceAfter /* saldo da variação × local × lote (F1.7) */;
  source?: { type: SourceType; id; number?: number }; userName; note? }
```

## T9. Ajuste / perda / saldo de abertura (drawer)
Campos: variação (busca), local, lote (se controla; na entrada pode criar lote com código + validade), tipo
(entrada/saída), motivo (Saldo de abertura, Ajuste, Quebra, Vencimento, Furto, Uso interno), quantidade, observação
(obrigatória em Ajuste). Mostra saldo atual do local antes de confirmar.
Regras: saída não deixa negativo se o produto não permite (RN-CE32); perdas não contam como demanda (RN-CE24 / previsão);
entrada manual com custo: só "Saldo de abertura" informa custo (entra no custo médio).
F1.6: aberto pela aba Estoque do T3 ("Ajuste ou perda"), com variação e local da matriz da loja do topo. O sentido é fixo
por motivo (abertura = entrada; quebra, vencimento, furto e uso interno = saída); só o Ajuste deixa escolher. Qualquer outro
motivo (venda, compra, devoluções, transferência, inventário) → 422 em `reason` (RN-CE02). `unitCost` fora do saldo de
abertura → 422 em `unitCost` (L5); Ajuste sem observação → 422 em `note` (L4); saída que deixa negativo → 422 em `quantity`
(RN-CE32). F1.7: produto com lote exige `lotId` ou `newLot` (só na entrada, nunca os dois) na entrada; na saída, sem lote, baixa por FEFO; lote em produto sem lote → 422 em `lotId`; código existente com outra validade → 422 em `newLot.code`. Lotes do seletor: `GET /api/stock/lots/options?variantId&locationId` → `{ id; code; expiresOn; quantity }[]`. Sem editar nem excluir: correção é lançamento
contrário (RN-CE14; RN-CE03 obsoleta).
```ts
POST /api/stock-movements/manual   ← ManualMovementDto   → 204   // API: ManualMovementRequestDto
POST /api/stock-transfers  { fromLocationId; toLocationId; note?; items: [{ variantId; quantity }] } → 201 StockTransferDto
     // F3.4b, RN-CE62: saída TransferOut por FEFO e entrada TransferIn nos mesmos lotes, sem custo; 422 em items[i].quantity
     // sem saldo, toLocationId igual à origem ou inativo. GET /api/stock-transfers/{id}. Tela: "Transferir" na aba Estoque do T3
ManualMovementDto { variantId; locationId; lotId?; newLot?: { code /* até 40 */; expiresOn } /* só entrada */; type: MovementType; reason: MovementReason; quantity /* > 0 */; unitCost? /* só Opening, > 0 */; note? /* obrigatória em Adjustment, até 500 */ }
```

## T10. Transferências (`/stock-transfers`)
Lista: nº, origem, destino, status, nº de itens, criada em/por, recebida em. Filtros: status, local, período.
Criar: origem, destino (≠ origem), itens (variação, lote se controla, quantidade; mostra disponível na origem).
Fluxo (visão Admin): Rascunho → **Enviar** (gera saídas) → **Receber** (gera entradas) ou Cancelar (só em Rascunho; se Enviada, cancelar devolve à origem).
Pode nascer de uma recomendação "Transferir" (RN-DF16) já preenchida.
```ts
StockTransferListItemDto { id; number; fromLocationName; toLocationName; status: TransferStatus; itemCount; createdAt; createdByName; receivedAt? }
StockTransferDetailDto { id; number; version; fromLocation: LocationOptionDto; toLocation: LocationOptionDto; status; note?;
  items: { id; variantId; productName; variantLabel; lotId?; lotCode?; quantity; availableAtOrigin }[]; forecastRecommendationId? }
SaveStockTransferDto { fromLocationId; toLocationId; note?; items: { variantId; lotId?; quantity }[]; version? }
POST /api/stock-transfers/{id}/send | /receive | /cancel   { version }
```

## T11. Inventário (`/inventory-counts`)
Lista: nº, local, escopo (total/categoria), status, abertura, fechamento, divergências.
Abrir: local + escopo. A API congela o **esperado** por variação/lote naquele momento.
Contar: tabela com produto, variação, lote, esperado (pode ser escondido para contagem "cega" — **lacuna L2**), contado (input), diferença.
Fechar: gera um ajuste por item com diferença (motivo "Ajuste de inventário"), mostra resumo (itens, valor da diferença a custo médio).
Movimentações durante a contagem: **lacuna L3**.
```ts
InventoryCountDetailDto { id; number; version; locationName; scope; categoryName?; status; startedAt; closedAt?;
  items: { id; productName; variantLabel; lotCode?; expected; counted?; difference?; differenceValue? }[] }
PUT  /api/inventory-counts/{id}/items  { version; items: { id; counted }[] }
POST /api/inventory-counts/{id}/close  { version }
```

## T12. Lotes vencendo (`/lots/expiring`)
Lista: produto, variação, lote, local, validade, dias, quantidade, valor a custo. Filtros: até N dias (padrão 30), local, categoria.
Ações: criar promoção (vendas), lançar perda por vencimento (T9).

## T13. Política de estoque (`/settings/stock-policy`)
Tabela das classes A, B, C: cobertura alvo (dias), dias de segurança; mostra quantos produtos em cada classe e a regra da classe
(A = 80% da receita, B = próximos 15%, C = 5%; recalculada a cada análise, RN-CE29).
```ts
GET /api/stock-policies        → StockPolicyDto[]   // F1.8; A, B, C do seed (A 15/7, B 30/5, C 45/3), sem criar nem inativar
PUT /api/stock-policies/{id}   ← { targetCoverageDays; safetyDays } /* inteiros 0–365 */ → StockPolicyDto
StockPolicyDto { id; abcClass; targetCoverageDays; safetyDays; productCount /* produtos ativos na classe; 0 até a F3 */ }
```
> F1.8: o DTO ganhou `id` para o PUT seguir a base de update (ADR 0010); a classe continua única (índice único).

## T14. "Cliente procurou e não tinha" (dialog)
Na busca de produto da venda rápida e na aba Estoque: variação, quantidade (padrão 1), local (loja selecionada). Um clique (RN-CE24).
`POST /api/lost-demand { variantId; locationId; quantity }`

---
## Enums novos (espelhar em `types/enums.ts`)
`ProductType` Standard=1, Apparel=2, Perishable=3, Bulk=4 · `Lifecycle` Active=1, Discontinued=2 · `SaleUnit` Unit=1, Kilogram=2, Liter=3, Meter=4 ·
`MovementType` In=1, Out=2 · `MovementReason` Opening=1, Purchase=2, Sale=3, CustomerReturn=4, SupplierReturn=5, TransferIn=6, TransferOut=7, CountAdjustment=8, Adjustment=9, Breakage=10, Expired=11, Theft=12, InternalUse=13 ·
`SourceType` Order=1, PurchaseOrder=2, Transfer=3, InventoryCount=4, Manual=5 · `TransferStatus` Draft=1, Sent=2, Received=3, Canceled=4 ·
`InventoryStatus` Open=1, Closed=2, Canceled=3 · `EventScope` National=1, Company=2 · `DateRule` Fixed=1, Easter=2, NthWeekday=3, BlackFriday=4, EasterOffset=5

## Lacunas encontradas neste módulo
- **L1** Referência a valor de atributo novo na mesma requisição: `tempKey`, resolvida na F1.3 (RN-CE50).
- **L2** Contagem de inventário "cega" (sem mostrar o esperado)? Recomendação: sim, opção ao abrir.
- **L3** Venda durante inventário aberto: recomendação — permitir; a API ajusta o esperado com as movimentações após a abertura.
- **L4** Motivo "Ajuste" genérico (além de quebra, furto etc.) é necessário? **Decidido (F1.6):** sim, com observação obrigatória.
- **L5** Saldo de abertura com custo: entra no custo médio. **Decidido (F1.6):** só o saldo de abertura informa custo.
