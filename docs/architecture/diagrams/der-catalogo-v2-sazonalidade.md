# DER — Catálogo v2 e dados para a sazonalidade (proposta)

> **Status:** proposta de 28/10/2026 a partir das respostas validadas RN-CE16 a RN-CE29 · substitui a parte 1 de `der-catalogo-estoque.md`

## Perfil de produto (`product_type`) — resposta ao item 5
O tipo define os padrões e os campos que a tela mostra, sem tabelas diferentes:
| Tipo | Liga por padrão | Campos que aparecem |
|--|--|--|
| Standard (papelaria, utilidades) | — | básico |
| Apparel (roupa, calçado) | `has_variants` | grade, coleção |
| Perishable (padaria, doces) | `tracks_lots`, `shelf_life_days` | lote, validade, unidade kg |
| Bulk (tecido, granel) | `sale_unit` = Meter/Kilogram | casas decimais, embalagem (rolo) |

## Como cada tabela alimenta a análise
- `product_sales_monthly` passa a ter, por mês: vendido, vendido em promoção, dias sem estoque, demanda perdida e preço médio.
  Assim o cálculo separa "vendeu porque era época" de "vendeu porque estava barato" e "não vendeu porque faltou".
- `stock_daily_snapshots`: saldo de fechamento por dia; 0 = dia sem estoque (job diário ou derivado das movimentações).
- `calendar_events` + `product_events`: datas do horizonte e quais produtos cada evento puxa (`lead_days` = antecedência).
- `lifecycle = Discontinued` nunca recebe "Comprar"; `shelf_life_days` limita a quantidade; `product_suppliers` traz prazo, mínimo e múltiplo.
- `abc_class` é recalculada a cada análise e escolhe a política (`stock_policies`) quando o produto não tem exceção.

## Catálogo v2

```mermaid
erDiagram
  categories |o--o{ categories : "pai (2 níveis)"
  categories ||--o{ category_products : ""
  products ||--o{ category_products : ""
  collections |o--o{ products : "coleção/temporada"
  products ||--|{ product_variants : ""
  products ||--o{ product_attributes : "grade"
  product_attributes ||--|{ product_attribute_values : ""
  product_variants ||--o{ product_variant_values : ""
  product_attribute_values ||--o{ product_variant_values : ""
  products ||--o{ product_events : ""
  calendar_events ||--o{ product_events : "puxa a venda"
  products ||--o{ product_suppliers : ""
  suppliers ||--o{ product_suppliers : ""
  stock_policies |o--o{ products : "classe ABC"

  products {
    uuid id PK
    string name
    string brand
    string description
    enum product_type "Standard, Apparel, Perishable, Bulk: define campos da tela"
    enum sale_unit "Unit, Kilogram, Liter, Meter"
    smallint decimal_places
    bool allows_negative "RN-CE32"
    bool has_variants "derivado: há atributo (RN-CE48)"
    bool tracks_lots
    int shelf_life_days "perecível; nulo = não vence"
    uuid collection_id FK "opcional"
    enum lifecycle "Active, Discontinued"
    date launched_on
    char abc_class "calculada: A, B, C. Coluna entra com stock_policies (F1.8)"
    int target_coverage_days "nulo = usa a política da classe. Coluna entra na F1.8"
    string image_key "chave no storage, nunca a URL (ADR 0006)"
    bool is_active
  }
  categories {
    uuid id PK
    uuid parent_id FK "nulo = nível 1"
    string name "único entre irmãs"
    string description
    bool is_active
  }
  collections {
    uuid id PK
    string name "Verão 2026, único"
    date starts_on
    date ends_on
    bool is_active
  }
  calendar_events {
    uuid id PK
    string name "Páscoa, Festa da Uva, único"
    enum scope "National, Company"
    enum date_rule "Fixed, Easter, NthWeekday, BlackFriday, EasterOffset"
    smallint month "Fixed e NthWeekday"
    smallint day "Fixed"
    smallint weekday "NthWeekday: 0 = domingo a 6 = sábado"
    smallint nth "NthWeekday: 1 a 4"
    smallint easter_offset_days "EasterOffset: -60 a 60"
    smallint lead_days "quantos dias antes a venda sobe"
    bool is_active
  }
  product_events {
    uuid product_id PK,FK
    uuid event_id PK,FK
  }
  product_suppliers {
    uuid id PK
    uuid product_id FK
    uuid supplier_id FK
    bool is_preferred
    string supplier_sku
    int lead_time_days "nulo = do fornecedor"
    decimal min_order_qty
    decimal order_multiple "compra de N em N, na unidade de venda"
    decimal last_cost
  }
  stock_policies {
    char abc_class PK "A, B, C"
    int target_coverage_days
    int safety_days
  }
  product_variants {
    uuid id PK
    uuid product_id FK
    string sku UK "único sem diferenciar maiúsculas, lower(sku)"
    string barcode UK "opcional; único em lower(barcode)"
    decimal price
    smallint sort_order "ordem da grade"
    bool is_active
    decimal average_cost "coluna entra na F1.5, com o livro-razão"
  }
  product_attributes {
    uuid id PK
    uuid product_id FK
    string name
    smallint sort_order
  }
  product_attribute_values {
    uuid id PK
    uuid attribute_id FK
    string value
    smallint sort_order
  }
  product_variant_values {
    uuid id PK
    uuid variant_id FK "UK com attribute_value_id"
    uuid attribute_value_id FK
  }
  category_products {
    uuid id PK
    uuid category_id FK "UK com product_id"
    uuid product_id FK
  }
```

**Decisões da F1.3:** `sort_order` volta de `der-catalogo-estoque.md`, porque a ordem P, M, G é da grade e o rótulo depende dela; também nas variações. Tabelas de vínculo com `id` e índice único, como `user_stores`. `default_min_quantity` e as colunas acima marcadas ficam para a fatia que as usa. Cascata de `products` para atributos, valores, variações e vínculos existe para a sincronização do formulário (RN-CE51); `products` em si nunca é apagado.

## Dados para a sazonalidade

```mermaid
erDiagram
  product_variants ||--o{ price_history : "preço ao longo do tempo"
  product_variants ||--o{ order_items : ""
  promotions |o--o{ order_items : "vendido em promoção"
  product_variants ||--o{ stock_daily_snapshots : ""
  stock_locations ||--o{ stock_daily_snapshots : ""
  product_variants ||--o{ lost_demand_records : ""
  stock_locations ||--o{ lost_demand_records : ""
  products ||--o{ product_sales_monthly : "agregado para a análise"
  calendar_events ||--o{ forecast_event_context : ""
  forecast_runs ||--o{ forecast_event_context : "eventos do horizonte"

  price_history {
    uuid id PK
    uuid variant_id FK
    decimal price
    date valid_from
    date valid_to "nulo = vigente"
    uuid changed_by FK
  }
  order_items {
    uuid id PK
    uuid variant_id FK
    decimal list_price "preço de tabela no dia"
    decimal unit_price "preço cobrado"
    uuid promotion_id FK "nulo = preço cheio"
    decimal quantity
  }
  stock_daily_snapshots {
    uuid variant_id PK,FK
    uuid location_id PK,FK
    date day PK
    decimal closing_quantity "0 = dia sem estoque"
  }
  lost_demand_records {
    uuid id PK
    uuid variant_id FK
    uuid location_id FK
    decimal quantity
    uuid recorded_by FK
    datetime created_at
  }
  product_sales_monthly {
    uuid product_id PK,FK
    smallint year PK
    smallint month PK
    decimal quantity_sold
    decimal quantity_sold_on_promo
    smallint days_out_of_stock
    decimal lost_demand_qty
    decimal avg_price
    decimal revenue
  }
  forecast_event_context {
    uuid forecast_run_id PK,FK
    uuid event_id PK,FK
    date event_date
  }
```

