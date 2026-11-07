# DER consolidado do Nextflow (proposta)

> **Status:** proposta de 28/10/2026, consolidando as entrevistas de estoque, produto, vendas e compras · a validar
> Partes detalhadas: `der-catalogo-v2-sazonalidade.md` (catálogo + dados da sazonalidade), `der-catalogo-estoque.md`
> (parte 2: estoque, lojas e locais). Imagens: `der-0` a `der-7`.

## Mudanças em relação ao banco atual (branch `task-17`)
| Hoje | Proposta | Motivo |
|--|--|--|
| Item de pedido/compra aponta para `products` | aponta para `product_variants` | grade (RN-CE34) |
| `products.quantity` | `stock_balances` por variação × local × lote | depósitos e lotes (RN-CE09) |
| `stock_movements` com tipo simples | livro-razão com motivo, origem, custo e saldo após | rastreabilidade e sazonalidade (RN-CE14) |
| `CostPrice` = último custo | `average_cost` + `last_cost` na variação | custo médio (RN-CE31) |
| `orders` exige cliente | cliente opcional, `channel` Counter/Order | balcão (RN-VD15) |
| Status Budget/PendingPayment/PaymentConfirmed/Canceled/Refunded | Budget/Paid/Canceled/Refunded/Expired | dois estados de negócio (RN-VD16) |
| `sales` (1:1 com pedido) + `payments` | `payments` direto no pedido; `sales` removida | a venda é o pedido pago |
| Análise sob demanda, IA com até 40 produtos | job semanal + manual, IA em lotes sequenciais (`forecast_ai_batches`), `notifications` | RN-DF18, RN-DF20 |
| Recomendação Buy/Promote/Hold por produto | + Transfer, itens por variação e local, acerto medido | RN-DF16, rateio pela grade, `forecast_accuracy` |
| Categoria plana | `parent_id` (2 níveis) | RN-CE23 |

## Mapa geral

```mermaid
erDiagram
  users ||--o{ orders : "vendeu"
  clients |o--o{ orders : "cliente opcional"
  stores ||--|{ stock_locations : ""
  stores ||--o{ orders : ""
  orders ||--|{ order_items : ""
  orders ||--o{ payments : ""
  order_items }o--|| product_variants : ""
  order_items }o--o| promotions : ""
  promotions }o--|| product_variants : ""
  products ||--|{ product_variants : ""
  products }o--o{ categories : "category_products"
  products }o--o| collections : ""
  products }o--o{ calendar_events : "product_events"
  products }o--o{ suppliers : "product_suppliers"
  product_variants ||--o{ price_history : ""
  product_variants ||--o{ lots : ""
  product_variants ||--o{ stock_balances : ""
  stock_locations ||--o{ stock_balances : ""
  stock_movements }o--|| product_variants : ""
  stock_movements }o--|| stock_locations : ""
  stock_transfers ||--|{ stock_transfer_items : ""
  inventory_counts ||--|{ inventory_count_items : ""
  suppliers ||--o{ purchase_orders : ""
  stock_locations ||--o{ purchase_orders : "entregar em"
  purchase_orders ||--|{ purchase_items : ""
  purchase_items }o--|| product_variants : ""
  clients ||--o{ addresses : ""
  suppliers ||--o{ addresses : ""
  addresses }o--|| cities : ""
  cities }o--|| states : ""
  states }o--|| countries : ""
  products ||--o{ product_sales_monthly : ""
  forecast_runs ||--o{ forecast_recommendations : ""
  forecast_runs ||--o{ forecast_projections : ""
  forecast_recommendations }o--|| products : ""
  forecast_recommendations ||--o{ forecast_recommendation_items : "quantidade por variação"
  forecast_recommendations |o--o| purchase_orders : "Comprar"
  forecast_recommendations |o--o| promotions : "Promover"
  forecast_recommendations |o--o| stock_transfers : "Transferir"
  forecast_projections ||--o| forecast_accuracy : "previsto x realizado"
```

## Vendas

```mermaid
erDiagram
  stores ||--o{ orders : ""
  stock_locations ||--o{ orders : "baixa daqui"
  clients |o--o{ orders : "opcional (balcão)"
  users ||--o{ orders : "quem vendeu"
  orders ||--|{ order_items : ""
  orders ||--o{ payments : ""
  product_variants ||--o{ order_items : ""
  promotions |o--o{ order_items : ""
  product_variants ||--o{ promotions : ""

  orders {
    uuid id PK
    int number UK "nº sequencial visível"
    uuid store_id FK
    uuid sale_location_id FK
    uuid client_id FK "nulo = balcão"
    uuid user_id FK
    enum channel "Counter, Order: venda rápida ou pedido"
    enum status "Budget, Paid, Canceled, Refunded, Expired"
    date valid_until "orçamento"
    decimal subtotal
    decimal discount_total "soma dos descontos dos itens"
    decimal total
    datetime paid_at
    datetime refunded_at
    string cancel_reason
  }
  order_items {
    uuid id PK
    uuid order_id FK
    uuid variant_id FK
    uuid lot_id FK "preenchido na baixa (FEFO)"
    decimal quantity
    decimal list_price
    decimal unit_price
    decimal discount "R$ por item"
    uuid promotion_id FK
    decimal unit_cost "custo médio no momento da venda"
  }
  payments {
    uuid id PK
    uuid order_id FK
    enum method "Cash, Credit, Debit, Pix, Transfer"
    decimal amount
    datetime created_at
  }
  promotions {
    uuid id PK
    uuid variant_id FK "nulo = todas as variações do produto"
    uuid product_id FK
    decimal discount_percent
    date start_date
    date end_date
    enum source "Manual, AiRecommendation"
    bool below_cost_confirmed
    bool is_active
  }
```

## Previsão

```mermaid
erDiagram
  forecast_runs ||--o{ forecast_recommendations : ""
  forecast_runs ||--o{ forecast_projections : ""
  products ||--o{ forecast_recommendations : ""
  forecast_recommendations ||--o{ forecast_recommendation_items : "rateio pela grade"
  product_variants ||--o{ forecast_recommendation_items : ""
  stock_locations |o--o{ forecast_recommendation_items : "Transferir: origem/destino"
  forecast_recommendations |o--o| purchase_orders : "aplicada como compra"
  forecast_recommendations |o--o| promotions : "aplicada como promoção"
  forecast_recommendations |o--o| stock_transfers : "aplicada como transferência"
  products ||--o{ forecast_projections : ""
  forecast_projections ||--o| forecast_accuracy : ""
  products ||--o{ product_seasonality : ""
  forecast_runs ||--o{ forecast_ai_batches : "lotes enviados à IA"
  forecast_runs ||--o{ notifications : "recomendações novas"
  users ||--o{ notifications : ""

  forecast_runs {
    uuid id PK
    enum trigger "Manual, Scheduled (semanal)"
    smallint horizon_months "auto: maior lead time + 3, máx. 6"
    enum status "Completed, CompletedWithoutAi, Failed"
    string ai_model
    string summary
    int products_analyzed
    int products_sent_to_ai
    datetime created_at
  }
  forecast_recommendations {
    uuid id PK
    uuid forecast_run_id FK
    uuid product_id FK
    enum action "Buy, Promote, Hold, Transfer"
    enum priority "Low, Medium, High"
    enum confidence "Low, Medium, High"
    enum status "Pending, Applied, Dismissed, Expired"
    decimal suggested_quantity
    decimal suggested_discount
    date deadline "comprar até"
    string reason "texto da IA ou template"
    bool ai_adjusted
  }
  forecast_recommendation_items {
    uuid id PK
    uuid recommendation_id FK
    uuid variant_id FK
    uuid from_location_id FK "só Transferir"
    uuid to_location_id FK
    decimal quantity
  }
  forecast_projections {
    uuid id PK
    uuid forecast_run_id FK
    uuid product_id FK
    smallint year
    smallint month
    decimal projected_quantity
  }
  forecast_accuracy {
    uuid projection_id PK,FK
    decimal actual_quantity
    decimal abs_error
    decimal pct_error
    datetime measured_at
  }
  product_seasonality {
    uuid product_id PK,FK
    smallint month PK
    decimal seasonal_index
    smallint months_of_history
  }
  forecast_ai_batches {
    uuid id PK
    uuid forecast_run_id FK
    smallint batch_number
    int products_count
    enum status "Pending, Sent, Completed, Failed"
    string error_message
    int duration_ms
  }
  notifications {
    uuid id PK
    uuid user_id FK
    enum type "NewRecommendations, LotExpiring, LowStock"
    string title
    string link "ex.: /forecast"
    string source_type
    uuid source_id
    datetime read_at "nulo = não lida"
    datetime created_at
  }
```

## Cadastros e acesso

```mermaid
erDiagram
  users ||--o{ orders : ""
  clients ||--o{ addresses : "owner"
  suppliers ||--o{ addresses : "owner"
  clients ||--o{ contacts : "owner"
  suppliers ||--o{ contacts : "owner"
  addresses }o--|| cities : ""
  cities }o--|| states : ""
  states }o--|| countries : ""

  stores {
    uuid id PK
    string name
    uuid default_sale_location_id FK "nulo no modelo; FK adiada, preenchida no mesmo commit"
    uuid default_receive_location_id FK "nulo no modelo; FK adiada, preenchida no mesmo commit"
    bool is_active
  }
  stock_locations {
    uuid id PK
    uuid store_id FK
    string name
    bool is_sellable
    bool is_active
  }
  user_stores {
    uuid id PK
    uuid user_id FK
    uuid store_id FK
  }
  users {
    uuid id PK
    string name
    string last_name
    date birth_date
    string email UK
    string cpf UK
    string password_hash
    enum role "Admin (único por ora)"
    bool is_active
    datetime last_login_at "nulo até o primeiro login"
  }
  clients {
    uuid id PK
    string name
    string last_name "opcional"
    string cpf UK "opcional; único quando informado"
    date birth_date "opcional"
    bool is_active
  }
  suppliers {
    uuid id PK
    string name
    string cnpj UK
    int lead_time_days "padrão; exceção em product_suppliers"
    string note "opcional"
    bool is_active
  }
  addresses {
    uuid id PK
    uuid owner_id
    enum owner_type "Client, Supplier"
    string zip_code
    string street
    string number
    string complement "opcional"
    string neighborhood
    uuid city_id FK
    bool is_main "um por dono"
  }
  contacts {
    uuid id PK
    uuid owner_id
    enum owner_type
    enum type "Phone, Email, WhatsApp"
    string value
    bool is_main "um por dono"
  }
```

