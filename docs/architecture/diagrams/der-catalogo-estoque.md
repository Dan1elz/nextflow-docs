# DER — Catálogo e Estoque (proposta)

> **Status:** proposta de 28/10/2026, a validar com o Daniel · Base: rodada de estoque (itens 1 a 7) e lojas × locais
> Nomes de tabela e coluna seguem o padrão do código (inglês, snake_case plural).

## Fronteiras entre módulos (para não virar "ninho de rato")
| Módulo | Dono das tabelas | Quem pode ler | Quem pode escrever |
|--|--|--|--|
| Catálogo | `products`, `product_variants`, `product_attributes`, `product_attribute_values`, `product_variant_values`, `categories` | todos | só o Catálogo; `average_cost`/`last_cost` só pelo Estoque |
| Estoque | `stores`, `stock_locations`, `user_stores`, `lots`, `stock_balances`, `stock_location_minimums`, `stock_movements`, `stock_transfers*`, `inventory_counts*` | todos | **só o Estoque**, por um único serviço (`IStockLedger`) |
| Vendas / Compras | `orders*`, `purchase_*` | todos | o próprio módulo; mexem no estoque **chamando** o `IStockLedger`, nunca gravando saldo |

Regras de modelagem:
1. **Livro-razão:** `stock_movements` é a verdade e nunca é editado nem apagado (erro se corrige com movimento contrário).
   `stock_balances` é o saldo materializado, atualizado na mesma transação que grava o movimento, com `version` para concorrência.
2. **Tudo é variação:** produto sem grade tem uma variação padrão oculta. Venda, compra e estoque sempre apontam para `product_variants`.
3. **Reserva não é gravada:** disponível = `stock_balances.quantity` − itens de orçamentos válidos (`orders.valid_until`) da mesma loja.
4. **Quantidade em unidade de venda:** compra e venda sempre na unidade de venda (RN-CE30); sem conversão de embalagem.
5. **Custo médio por variação na empresa** (não por local); transferência não altera custo.
6. **Origem rastreável:** todo movimento tem `source_type` + `source_id` (pedido, compra, transferência, contagem) e `user_id`.

## 1 — Catálogo (SUBSTITUÍDA por `der-catalogo-v2-sazonalidade.md`; sem embalagem desde RN-CE30)

```mermaid
erDiagram
  categories ||--o{ category_products : ""
  products ||--o{ category_products : ""
  products ||--|{ product_variants : "1 produto, N variações (mín. 1)"
  products ||--o{ product_attributes : "eixos da grade"
  product_attributes ||--|{ product_attribute_values : "P, M, G"
  product_variants ||--o{ product_variant_values : ""
  product_attribute_values ||--o{ product_variant_values : ""
  products ||--o{ product_packagings : "unidade de compra"
  suppliers |o--o{ product_packagings : "embalagem do fornecedor"

  categories {
    uuid id PK
    string name
    bool is_active
  }
  category_products {
    uuid category_id PK,FK
    uuid product_id PK,FK
  }
  products {
    uuid id PK
    string name
    string brand
    enum sale_unit "Unit, Kg, Meter, Liter"
    smallint decimal_places "0 un, 3 kg, 2 m"
    bool tracks_lots
    bool allows_negative
    bool has_variants "false = 1 variação padrão oculta"
    bool is_active
  }
  product_attributes {
    uuid id PK
    uuid product_id FK
    string name "Tamanho, Cor"
    smallint sort_order
  }
  product_attribute_values {
    uuid id PK
    uuid attribute_id FK
    string value "P, Azul"
    smallint sort_order
  }
  product_variants {
    uuid id PK
    uuid product_id FK
    string sku UK
    string barcode UK "nulo permitido"
    decimal price
    decimal average_cost "custo médio"
    decimal last_cost
    bool is_active
  }
  product_variant_values {
    uuid variant_id PK,FK
    uuid attribute_value_id PK,FK
  }
  product_packagings {
    uuid id PK
    uuid product_id FK
    uuid supplier_id FK "nulo = qualquer"
    string name "Caixa 12, Rolo 50 m"
    decimal factor "12, 50"
    string barcode
  }
```

## 2 — Estoque, lojas e locais

```mermaid
erDiagram
  stores ||--|{ stock_locations : "loja tem locais"
  stores ||--o{ user_stores : ""
  users ||--o{ user_stores : "lojas que acessa"
  stock_locations ||--o{ stock_balances : ""
  product_variants ||--o{ stock_balances : "saldo por variação x local x lote"
  product_variants ||--o{ lots : ""
  lots |o--o{ stock_balances : ""
  stock_locations ||--o{ stock_movements : ""
  product_variants ||--o{ stock_movements : ""
  lots |o--o{ stock_movements : ""
  users ||--o{ stock_movements : "quem fez"
  stock_transfers ||--|{ stock_transfer_items : ""
  stock_transfer_items ||--|{ stock_movements : "gera saída + entrada"
  inventory_counts ||--|{ inventory_count_items : ""
  inventory_count_items |o--o| stock_movements : "gera ajuste"
  stock_locations ||--o{ inventory_counts : ""
  stock_locations ||--o{ stock_location_minimums : ""
  product_variants ||--o{ stock_location_minimums : ""

  stores {
    uuid id PK
    string name
    uuid default_sale_location_id FK "de onde a venda baixa"
    uuid default_receive_location_id FK "onde a compra entra"
    bool is_active
  }
  stock_locations {
    uuid id PK
    uuid store_id FK
    string name "Prateleira, Depósito"
    bool is_sellable
    bool is_active
  }
  user_stores {
    uuid user_id PK,FK
    uuid store_id PK,FK
  }
  lots {
    uuid id PK
    uuid variant_id FK
    string code
    date expires_on
  }
  stock_balances {
    uuid id PK
    uuid variant_id FK "UK com location+lot"
    uuid location_id FK
    uuid lot_id FK "nulo sem lote"
    decimal quantity "físico"
    int version "concorrência otimista"
  }
  stock_location_minimums {
    uuid variant_id PK,FK
    uuid location_id PK,FK
    decimal min_quantity
  }
  stock_movements {
    uuid id PK
    uuid variant_id FK
    uuid location_id FK
    uuid lot_id FK
    enum type "In, Out"
    enum reason "Purchase, Sale, CustomerReturn, SupplierReturn, TransferIn, TransferOut, CountAdjustment, Loss, InternalUse, Opening"
    decimal quantity "com sinal: entrada > 0, saída < 0"
    decimal unit_cost
    decimal balance_after
    string source_type "Order, PurchaseOrder, Transfer, Count"
    uuid source_id
    string note
    uuid user_id FK
    datetime created_at
  }
  stock_transfers {
    uuid id PK
    uuid from_location_id FK
    uuid to_location_id FK
    enum status "Draft, Sent, Received, Canceled"
    uuid created_by FK
    datetime created_at
  }
  stock_transfer_items {
    uuid id PK
    uuid transfer_id FK
    uuid variant_id FK
    uuid lot_id FK
    decimal quantity
  }
  inventory_counts {
    uuid id PK
    uuid location_id FK
    enum scope "Full, Category"
    uuid category_id FK
    enum status "Open, Counting, Closed"
    datetime started_at
    datetime closed_at
  }
  inventory_count_items {
    uuid id PK
    uuid count_id FK
    uuid variant_id FK
    uuid lot_id FK
    decimal expected
    decimal counted
    uuid adjustment_movement_id FK
  }
```

## 3 — Pontos de contato com vendas e compras

```mermaid
erDiagram
  stores ||--o{ orders : "venda pertence a uma loja"
  stock_locations |o--o{ orders : "local de baixa (padrão da loja)"
  orders ||--|{ order_items : ""
  product_variants ||--o{ order_items : "vende variação, não produto"
  stores ||--o{ purchase_orders : ""
  stock_locations ||--o{ purchase_orders : "local de recebimento"
  purchase_orders ||--|{ purchase_items : ""
  product_variants ||--o{ purchase_items : ""

  orders {
    uuid id PK
    uuid store_id FK
    uuid sale_location_id FK
    uuid client_id FK "nulo = balcão"
    enum status
    date valid_until "orçamento: reserva até"
  }
  order_items {
    uuid id PK
    uuid order_id FK
    uuid variant_id FK
    decimal quantity
    decimal unit_price
    decimal discount "R$ por item"
  }
  purchase_orders {
    uuid id PK
    uuid store_id FK
    uuid receive_location_id FK
    uuid supplier_id FK
    enum status
  }
  purchase_items {
    uuid id PK
    uuid purchase_order_id FK
    uuid variant_id FK
    decimal quantity "sempre na unidade de venda"
    decimal unit_cost
  }
```

