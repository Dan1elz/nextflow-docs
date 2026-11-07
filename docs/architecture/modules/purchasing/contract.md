# Contrato — Compras e cadastros (fornecedores, clientes)

> **Status:** rascunho para validação · **Atualizado:** 2026-11-07 (F2.7) · Convenções: `../../contracts/README.md`
> Regras: `business-rules.md` (RN-CP*), `../registry/business-rules.md` (RN-CD*), `../catalog-inventory/business-rules.md` (RN-CE*)
> DER: `../../diagrams/der-consolidado.md`

Contexto global do front: **loja selecionada** no topo (`storeId`). Listagem de compras filtra pelo local de entrega dessa loja;
o padrão do local de entrega no formulário é `stores.defaultReceiveLocationId` (RN-CP07).

---

## T-CP1. Pedidos de compra — listagem (`/purchase-orders`)
**Carrega** (`PurchaseOrderListItemDto`): nº, fornecedor (nome), local de entrega (loja › local), status, nº de itens,
total, criado em, previsão de chegada (criado/enviado + prazo efetivo), recebido em, **lead time real** (dias, quando recebido),
badge "Gerado pela IA" (vínculo com recomendação, RN-DF15), badge "Atrasado" (pendente com previsão vencida).
**Filtros:** busca (nº, fornecedor), status, fornecedor, local de entrega, período de criação, "só da IA", "só atrasados".
**Ordenação:** nº, criado em, previsão de chegada, total.
**Ações:** novo (T-CP2), ver (T-CP3), editar (só Orçamento/Pendente), receber (T-CP4, só Pendente), cancelar (T-CP5).

```ts
GET /api/purchase-orders?offset&limit&filters&sort&order&storeId
PurchaseOrderListItemDto {
  id; number: number; supplierId; supplierName;
  receiveLocationId; receiveLocationName; storeName;
  status: PurchaseStatus; itemCount: number; total: number;
  createdAt; sentAt?; expectedOn?: DateOnly; receivedAt?; realLeadTimeDays?: number;
  isLate: boolean; fromForecast: boolean;
}
```

## T-CP2. Pedido de compra — criar / editar (`/purchase-orders/create`, `/:id/edit`)
**Cabeçalho:** fornecedor (combo ativo), local de entrega (combo de locais ativos; padrão da loja), observação.
Mostra o prazo efetivo do fornecedor e a **previsão de chegada** calculada.
**Itens** (uma linha por variação): busca de produto filtrada pelos produtos vinculados ao fornecedor (opção "mostrar todos");
ao escolher, a API devolve `PurchaseItemSuggestionDto` com: produto, variação, código no fornecedor, unidade de venda e casas
decimais, **pedido mínimo**, **múltiplo** (RN-CE27/CE30), último custo pago a esse fornecedor (custo sugerido), custo médio atual,
disponível na loja e a caminho (outras compras Orçamento/Pendente, RN-CP05).
Campos por linha: quantidade (unidade de venda, sem caixa, RN-CE30), custo unitário (editável), subtotal (calculado na API no save).
Para produto com grade: atalho "adicionar grade" abre a matriz de variações do produto com quantidade por variação.

**Validações:** fornecedor ativo; local ativo; ≥ 1 item (RN-CP01); quantidade > 0 e respeitando casas decimais;
quantidade ≥ mínimo e múltiplo do par produto × fornecedor — **aviso com confirmação** (`errors.confirm`), não bloqueio (L-CP2);
custo ≥ 0; produto "fora de linha" exige confirmação (RN-CE19); variação inativa bloqueia.
Edição só em Orçamento ou Pendente; recebido não altera (RN-CP03). `version` obrigatória no update.

**Ações de status:** Salvar (Orçamento) · **Enviar ao fornecedor** (Orçamento → Pendente, grava `sentAt`) · Receber (T-CP4) · Cancelar (T-CP5).

```ts
GET  /api/purchase-orders/{id}/form                      → PurchaseOrderFormDto
GET  /api/purchase-orders/item-suggestion?supplierId&variantId&storeId → PurchaseItemSuggestionDto
GET  /api/purchase-orders/variant-options?supplierId&search&onlyLinked=true&limit=20 → PurchaseVariantOptionDto[]   (F2.7: busca de itens; onlyLinked=false = "mostrar todos")
POST /api/purchase-orders/{id}/cancel { version; reason } → PurchaseOrderDetailDto
POST /api/purchase-orders            ← SavePurchaseOrderDto → PurchaseOrderDetailDto
PUT  /api/purchase-orders/{id}       ← SavePurchaseOrderDto → PurchaseOrderDetailDto
POST /api/purchase-orders/{id}/send  { version } → PurchaseOrderDetailDto

SavePurchaseOrderDto {
  supplierId; receiveLocationId; note?; version?; confirmWarnings?: boolean;
  items: { id?: string; variantId: string; quantity: number; unitCost: number }[];
}
PurchaseVariantOptionDto { variantId; productId; productName; variantLabel; sku; isLinked: boolean }   // F2.7
PurchaseItemSuggestionDto {
  variantId; productId; productName; variantLabel; sku; supplierSku?;
  saleUnit: SaleUnit; decimalPlaces: number; tracksLots: boolean; lifecycle: Lifecycle;
  minOrderQty?: number; orderMultiple?: number;
  lastCostFromSupplier?: number; averageCost?: number;
  availableAtStore: number; incomingQuantity: number;
}
PurchaseOrderFormDto = SavePurchaseOrderDto & { id; number; version; status; supplierName; leadTimeDays: number; expectedOn?: DateOnly; total;
  items: (SavePurchaseOrderDto['items'][number] & PurchaseItemSuggestionDto & { subtotal: number })[];
  options: { locations: LocationOptionDto[] } }
```

## T-CP3. Pedido de compra — visualizar (`/purchase-orders/:id/view`)
Cabeçalho (`PurchaseOrderDetailDto`): nº, status, fornecedor (nome, CNPJ, contato principal), local de entrega, criado por/em,
enviado em, previsão de chegada, recebido em/por, lead time real, total, observação, origem (link para a análise e a recomendação
quando veio da IA), motivo de cancelamento.
Itens: produto, variação, SKU, código no fornecedor, quantidade, custo unitário, subtotal; quando recebido: lote, validade e
**custo médio após a entrada**.
Linha do tempo: criado → enviado → recebido/cancelado, com usuário.

```ts
GET /api/purchase-orders/{id} → PurchaseOrderDetailDto
PurchaseOrderDetailDto { id; number; version; status: PurchaseStatus;
  supplier: { id; name; cnpj; mainContact?: string };
  receiveLocation: LocationOptionDto; note?; total; leadTimeDays: number;
  createdAt; createdByName; sentAt?; expectedOn?: DateOnly; receivedAt?; receivedByName?; realLeadTimeDays?;
  canceledAt?; cancelReason?;
  forecast?: { runId; recommendationId; runCreatedAt };
  items: { id; variantId; productId; productName; variantLabel; sku; supplierSku?; quantity; unitCost; subtotal;
           tracksLots: boolean; lots?: { lotCode; expiresOn: DateOnly; quantity }[]; averageCostAfter?: number }[] }
```

## T-CP4. Recebimento (dialog/página a partir de Pendente)
Lista todos os itens do pedido com quantidade pedida (somente leitura: **sem recebimento parcial**, RN-CP04).
Para item de produto com lote (RN-CE10): informar 1+ lotes (código, validade, quantidade) cuja soma = quantidade pedida.
Validade padrão sugerida = hoje + `shelfLifeDays` (editável). Data de recebimento = agora (não editável — L-CP4).
Ao confirmar, a API (via `IStockLedger`, decisão 0007): gera uma entrada (`reason = Purchase`) por item/lote no local de entrega,
recalcula `average_cost` e grava `last_cost` na variação e no produto × fornecedor (RN-CE31, RN-CP02), grava `receivedAt`
e o lead time real (RN-CP06), muda o status para Recebido. Tudo numa transação.
Divergência (veio menos/mais ou avariado): receber tudo e lançar ajuste/perda (T9 do estoque) — L-CP1.

```ts
POST /api/purchase-orders/{id}/receive
ReceivePurchaseOrderDto { version; items: { itemId; lots?: { code; expiresOn: DateOnly; quantity }[] }[] }
→ PurchaseOrderDetailDto
```
F2.8 (2026-11-07): só Pendente (senão 400); `items` traz cada item do pedido uma vez (senão 422 em `items`); versão velha → 409.
F1.7: item de produto com lote exige `lots[] { code (até 40); expiresOn; quantity > 0 }` somando a quantidade do item, sem código repetido (422 em `items[i].lots`); produto sem lote não recebe `lots` (422); código já existente na variação com outra validade → 422 em `items[i].lots[j].code` (mesma validade = mesmo lote). Uma entrada por lote; o detalhe (T-CP3) traz `lots { lotCode; expiresOn; quantity }` lidos das entradas. O último custo vai para
`ProductSupplier.lastCost` só quando o vínculo existe, e passa a preencher `lastCostFromSupplier` da sugestão.
`realLeadTimeDays` = dia de negócio do recebimento − dia de negócio do envio. Entrada simultânea com custo na mesma variação → 409.

## T-CP5. Cancelar pedido de compra (dialog)
Permitido em Orçamento e Pendente; nunca em Recebido (RN-CP03). Motivo obrigatório.
Cancelar não gera movimentação (nada entrou). A quantidade deixa de contar como "a caminho" (RN-CP05).
Se veio de recomendação da IA, a recomendação volta para Pendente? — **L-CP5**.
`POST /api/purchase-orders/{id}/cancel { version; reason }`

---

## T-CD1. Fornecedores — listagem (`/suppliers`)
**Carrega:** nome, CNPJ (formatado no front), cidade/UF do endereço principal, contato principal, prazo padrão (dias),
**lead time real médio** (últimos 5 recebidos, RN-CP06), nº de produtos vinculados, última compra, ativo.
**Filtros (`filters`):** `search` (nome, dígitos do CNPJ), `isActive`, `cityId`. **Ordenação:** `name`, `leadTimeDays`, `createdAt`.
**Ações:** novo, ver, editar, inativar/reativar (RN-CD04).
**Campos que dependem de tabelas futuras:** `realLeadTimeDays` (nulo) e `lastPurchaseOn` (nulo) até a fase 2; `productCount` (zero) até a fase 1.
```ts
GET    /api/suppliers?offset&limit&filters&sort&order → PaginationDto<SupplierListItemDto>
DELETE /api/suppliers/{id}             → 204   // inativa
PATCH  /api/suppliers/{id}/reactivate  → 204
SupplierListItemDto { id; name; cnpj; cityState?: string; mainContact?: string; leadTimeDays: number;
  realLeadTimeDays?: number; productCount: number; lastPurchaseOn?: DateOnly; isActive }
```

## T-CD2. Fornecedor — criar / editar / visualizar (`/suppliers/...`)
Abas (padrão `EntityTabsLayout`). Ao criar, só Dados fica habilitada; depois de salvar a tela abre a edição em Endereços.
| Aba | Carrega | Ações |
|--|--|--|
| Dados | nome, CNPJ (único e válido, RN-CD02), prazo padrão 1–180, padrão 7 (RN-CD03), observação | salvar |
| Endereços | CEP (preenche via ViaCEP, a cidade pelo código IBGE), rua, número, complemento, bairro, cidade/UF, principal | CRUD |
| Contatos | tipo (Telefone, E-mail, WhatsApp), valor, principal | CRUD |
| Produtos | Implementada em 07/11 (back 89d3c3c, front e007611): vínculos do fornecedor com produto, marca, código no fornecedor, preferido, prazo efetivo, mínimo, múltiplo e último custo (ver `SupplierProductDto` abaixo) | editar vínculo (mesmo DTO do T2 do catálogo) |
| Compras | Implementada em 07/11: pedidos do fornecedor pela listagem `GET /api/purchase-orders` filtrada por `supplierId`; o resumo "total comprado 12 meses" previsto não tem endpoint próprio | abrir pedido |

```ts
GET  /api/suppliers/{id} → SupplierResponseDto
POST /api/suppliers      SupplierRequestDto → 201 SupplierResponseDto
PUT  /api/suppliers/{id} SupplierRequestDto → SupplierResponseDto
SupplierRequestDto  { name; cnpj; leadTimeDays = 7; note? }
SupplierResponseDto { id; name; cnpj; leadTimeDays; note?; isActive; realLeadTimeDays? /* nulo até a fase 2 */;
  mainAddress?: AddressResponseDto; mainContact?: ContactResponseDto; createdAt; updatedAt? }
GET /api/suppliers/options?search → Option[]  // só ativos, até 20; label = nome · CNPJ

// 07/11 (89d3c3c), conferido no código:
GET /api/suppliers/{id}/products  → SupplierProductDto[]  { productId; productName; brand?; productIsActive; lifecycle; isPreferred; supplierSku?; leadTimeDays /* efetivo */; minOrderQty?; orderMultiple?; lastCost? }
// GET /api/suppliers/{id}/purchases não existe: a aba Compras usa GET /api/purchase-orders com filtro supplierId.
// Listagem GET /api/suppliers: filtros stateId, cityId, purchases (with|without|last30|last90|inactive90), pendingOrders;
// SupplierListItemDto traz realLeadTimeDays, productCount e lastPurchaseOn (ver registry/overview.md).
```

### Endereços e contatos (de cliente e fornecedor)
Polimórficos por `ownerType` + `ownerId`, sem FK para o dono: `CHECK` de `owner_type` no banco e existência do dono validada na API (404).
No máximo um principal por dono: marcar desmarca os outros, e o primeiro registro do dono já nasce principal; desmarcar ou excluir o principal não promove outro (RN-CD05, RN-CD06). Exclusão física.
Dono inativo: criar e editar devolvem 400 (RN-CD10).
Listar sem `ownerType` e `ownerId` válidos em `filters` devolve 400. O dono não muda na edição.
```ts
GET    /api/addresses?filters={"ownerType":"Client","ownerId":"..."} → PaginationDto<AddressResponseDto>   // principal primeiro
POST   /api/addresses       AddressRequestDto → 201 AddressResponseDto
PUT    /api/addresses/{id}  UpdateAddressRequestDto → AddressResponseDto
DELETE /api/addresses/{id}  → 204
UpdateAddressRequestDto { zipCode; street; number; complement?; neighborhood; cityId; isMain }
AddressRequestDto extends UpdateAddressRequestDto { ownerType: OwnerType; ownerId }
AddressResponseDto { id; ownerType: OwnerType; ownerId; zipCode /* só dígitos */; street; number; complement?; neighborhood; cityId; cityName; stateAbbreviation; isMain }

GET    /api/contacts?filters={"ownerType":"Client","ownerId":"..."} → PaginationDto<ContactResponseDto>    // principal primeiro
POST   /api/contacts        ContactRequestDto → 201 ContactResponseDto
PUT    /api/contacts/{id}   UpdateContactRequestDto → ContactResponseDto
DELETE /api/contacts/{id}   → 204
UpdateContactRequestDto { type: ContactType; value; isMain }   // telefone e WhatsApp: 10 ou 11 dígitos; e-mail válido
ContactRequestDto extends UpdateContactRequestDto { ownerType: OwnerType; ownerId }
ContactResponseDto { id; ownerType: OwnerType; ownerId; type: ContactType; value /* telefone só com dígitos */; isMain }
```

### País, estado e cidade
Só leitura, com seed do IBGE (2 países, 27 estados, 5.570 municípios). Sem tela própria. Combos sem acento na busca não casam nomes acentuados.
```ts
GET /api/countries/options?search → Option[]                                    // até 20
GET /api/states/options?search&filters={"countryId":"..."} → Option[]           // até 50; label "São Paulo/SP"
GET /api/cities/options?search&filters={"stateId":"...","ibgeCode":"..."} → Option[]  // até 20; label "Campinas/SP"
```

## T-CD3. Clientes — listagem (`/clients`)
**Carrega:** nome completo, CPF (formatado), telefone principal, cidade/UF, nº de compras, total comprado, última compra, ativo.
`mainPhone` (e `phone` no combo) só vem do contato principal do tipo telefone ou WhatsApp: com zero principal ou principal e-mail fica nulo (RN-CD06).
**Filtros (`filters`):** `search` (nome, sobrenome, dígitos do CPF, telefone), `isActive`, `birthdaysThisMonth` (L-CP7, mês da data de negócio).
**Ordenação:** `fullName`, `birthDate`, `createdAt`. **Ações:** novo, ver, editar, inativar/reativar.
**Campos que dependem de tabelas futuras:** `orderCount` e `totalSpent` (zero), `lastPurchaseOn` (nulo) até a fase 2.
```ts
GET    /api/clients?offset&limit&filters&sort&order → PaginationDto<ClientListItemDto>
DELETE /api/clients/{id}             → 204   // inativa
PATCH  /api/clients/{id}/reactivate  → 204
ClientListItemDto { id; fullName; cpf?; birthDate?: DateOnly; mainPhone?; cityState?; orderCount; totalSpent; lastPurchaseOn?: DateOnly; isActive }
```

## T-CD4. Cliente — criar / editar / visualizar
Abas: **Dados** (nome, sobrenome, CPF opcional, único e válido quando informado, RN-CD01 e L-CP6; nascimento),
**Endereços**, **Contatos** (mesmos DTOs do fornecedor), **Compras** (**vazia com `Empty` até a fase 2**; depois: pedidos pagos/orçamentos:
nº, data, loja, status, total, itens; resumo: total, ticket médio, última compra).
Na venda, o cliente é **opcional** (RN-VD15); o combo de cliente da venda usa `GET /api/clients/options?search` → `ClientOptionDto`
e oferece "cadastro rápido" (nome + telefone) sem sair da venda. O telefone vira contato principal no mesmo commit. A API está pronta; a tela entra com a venda (F2.4).
```ts
GET  /api/clients/{id} → ClientResponseDto
POST /api/clients      ClientRequestDto → 201 ClientResponseDto
PUT  /api/clients/{id} ClientRequestDto → ClientResponseDto
POST /api/clients/quick QuickCreateClientRequestDto → 201 ClientOptionDto
ClientRequestDto { name; lastName?; cpf?; birthDate?: DateOnly }
ClientResponseDto { id; name; lastName?; cpf?; birthDate?; isActive; mainAddress?: AddressResponseDto; mainContact?: ContactResponseDto;
  orderCount; totalSpent; averageTicket; lastPurchaseOn? /* zero ou nulos até a fase 2 */; createdAt; updatedAt? }
ClientOptionDto { id; label /* "Ana Souza · 123.***.***-00" */; phone? }      // só ativos, até 20
QuickCreateClientRequestDto { name; phone }

// Fase 2 (ainda não existe)
GET /api/clients/{id}/orders?offset&limit → PaginationDto<OrderListItemDto>   // DTO do contrato de vendas
```

---
## Enums (espelhar em `types/enums.ts`)
`PurchaseStatus` Budget=1, Pending=2, Received=3, Canceled=4 (mantido) · `ContactType` e `OwnerType` trafegam como string: `Phone`, `Email`, `WhatsApp`;
`Client`, `Supplier`. Reusa `SaleUnit`, `Lifecycle` do catálogo.

## Lacunas encontradas neste módulo
- **L-CP1** Divergência no recebimento (faltou, sobrou, avariado): sem recebimento parcial, o fluxo é receber tudo e ajustar. Recomendação: botão "receber com divergência" que já abre o ajuste com motivo, para não depender de lembrar.
- **L-CP2** Mínimo e múltiplo do fornecedor: bloqueia ou avisa? Recomendação: avisar e confirmar (manual); a sugestão da IA já arredonda.
- **L-CP3** Lead time real conta da criação (hoje) ou do envio? Com o status "Enviar", recomendação: contar de `sentAt` (resolve a pergunta aberta de RN-CP06).
- **L-CP4** Data de recebimento retroativa (recebeu ontem, lançou hoje)? Recomendação: permitir até 7 dias para trás, porque afeta o lead time e o histórico da sazonalidade.
- **L-CP5** Cancelar compra gerada pela IA: a recomendação volta para Pendente ou fica Aplicada? Recomendação: volta para Pendente se a análise ainda for a mais recente; senão, nada.
- **L-CP6** CPF do cliente obrigatório? Com cliente opcional e cadastro rápido, decidido: opcional, único quando informado (RN-CD01, 2026-10-30).
- **L-CP7** Aniversário e observações do cliente (CRM-lite) entram? Decidido: só o filtro de aniversariantes, sem campanhas nem observações (RN-CD07, 2026-10-30).
- **L-CP8** Número sequencial visível (`number`) não existe hoje em compras nem transferências; precisa de sequência no banco. Compras: resolvido na F2.7 (coluna identidade do Postgres, 2026-11-07).
