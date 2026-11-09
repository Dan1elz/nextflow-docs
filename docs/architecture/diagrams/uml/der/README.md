# Diagramas entidade-relacionamento (DER)

> **Status:** rascunho para o TCC, gerado em 09/11/2026 do **banco real** (Postgres de dev com todas as migrations
> aplicadas, até `AddRecommendationStores`); aguarda revisão do Daniel. Feito em **Mermaid** (`erDiagram`), como os
> DERs anteriores, e substitui para o TCC os `der-*.png` de `../../` (feitos durante o desenho, antes de várias migrations).

48 tabelas e 82 chaves estrangeiras em **11 figuras por módulo** e um **mapa geral para o apêndice**.

## Figuras
| Figura sugerida | Arquivo | Tabelas |
|--|--|--|
| DER — Acesso e notificações | [der-1-acesso.png](der-1-acesso.png) | users, user_stores, notifications |
| DER — Cadastros de pessoas e localidade | [der-2-cadastros.png](der-2-cadastros.png) | clients, suppliers, addresses, contacts, cities, states, countries |
| DER — Produto, variações e preço | [der-3-produto.png](der-3-produto.png) | products, product_variants, product_attributes, product_attribute_values, product_variant_values, price_history |
| DER — Classificação e fornecimento do produto | [der-4-classificacao.png](der-4-classificacao.png) | categories, category_products, collections, calendar_events, product_events, product_suppliers |
| DER — Lojas, locais, saldo e livro-razão | [der-5-estoque.png](der-5-estoque.png) | stores, stock_locations, stock_balances, lots, stock_movements, stock_location_minimums, stock_policies |
| DER — Transferência de estoque | [der-6-transferencia.png](der-6-transferencia.png) | stock_transfers, stock_transfer_items |
| DER — Vendas e promoções | [der-7-vendas.png](der-7-vendas.png) | orders, order_items, payments, promotions |
| DER — Pedidos de compra | [der-8-compras.png](der-8-compras.png) | purchase_orders, purchase_items |
| DER — Previsão: análise e recomendação | [der-9-previsao-analise.png](der-9-previsao-analise.png) | forecast_runs, forecast_recommendations, forecast_ai_batches, forecast_projections, forecast_settings |
| DER — Previsão: aplicação da recomendação | [der-10-previsao-aplicacao.png](der-10-previsao-aplicacao.png) | forecast_recommendation_items, forecast_recommendation_stores, forecast_recommendation_purchase_orders |
| DER — Dados derivados para a previsão | [der-11-dados-derivados.png](der-11-dados-derivados.png) | product_sales_monthly, product_seasonality, stock_daily_snapshots |
| **Apêndice** — Mapa geral dos módulos | [der-apendice-geral.png](der-apendice-geral.png) | as 48, agrupadas, com a contagem de FKs entre módulos |

Legenda no Word: "Figura N – Diagrama entidade-relacionamento (Módulo). Fonte: Elaborado pelo autor (2026)."

## Como ler (texto para pôr abaixo da figura no Word ou falar na banca)
- **Cor = módulo**, a mesma em todas as figuras: rosa Acesso, amarelo Cadastros, roxo Produto, verde Estoque,
  azul Vendas, laranja Compras, ciano Previsão. Uma tabela de outro módulo aparece só com a chave, na cor dela, e diz
  em qual figura está detalhada.
- **Nome em português e, entre parênteses, a tabela no banco:** "Saldo (stock_balances)".
- **Cada linha da tabela:** tipo, coluna, chave (**PK** primária, **FK** estrangeira) e um comentário com o significado
  dos códigos (ex.: `type` = "entrada ou saída") ou "opcional" quando a coluna aceita nulo.
- **Ligações em pé de galinha com um verbo**, lido de quem tem a chave primária para quem tem a FK:
  "Loja *possui* Local", "Local *guarda* Saldo". `||` exatamente um, `|o` zero ou um, `o{` zero ou muitos.
  Linha tracejada = ligação sem FK física (endereços e contatos podem ser de cliente **ou** de fornecedor).
- **Fora do desenho:** as colunas de auditoria (`created_at`, `updated_at`, `version`), presentes em quase todas as
  tabelas, e o tamanho dos campos (`varchar(100)`, `numeric(14,3)`), que estão em [`esquema/colunas.txt`](esquema/colunas.txt).

## Decisões de modelagem que o DER mostra (roteiro para a banca)
1. **Estoque por variação × local × lote** (`stock_balances`), sempre igual à soma do **livro-razão**
   (`stock_movements`), que nunca é editado nem apagado (ADR 0007, 0008, 0009). Figura 5.
2. **O livro-razão aponta para o documento de origem** por `source_type` + `source_id` (venda, pedido de compra,
   transferência, ajuste), sem FK física, para servir a todos os tipos de documento. Figura 5.
3. **Venda e pagamentos:** uma venda tem vários itens e várias formas de pagamento; o item guarda o preço de tabela,
   o preço praticado e a promoção aplicada. Figura 7.
4. **A recomendação da IA fica ligada ao que ela gerou** (pedidos de compra, um por loja; promoção; transferência) e
   guarda a parte de cada loja e de cada variação (RN-DF21, RN-DF27, RN-DF28). Figuras 9 e 10.
5. **Dados derivados** (venda mensal, sazonalidade, fotografia diária do estoque) são recalculados a partir das vendas
   e do estoque para alimentar a previsão; não são digitados. Figura 11.

## Dicionário dos enums (colunas `smallint`)
O comentário de cada coluna já diz o significado; os valores numéricos ficam aqui.

| Coluna | Enum | Valores |
|--|--|--|
| users.role | RoleEnum | 1 User, 2 Admin |
| addresses.owner_type, contacts.owner_type | OwnerTypeEnum | 1 Client, 2 Supplier |
| contacts.type | ContactTypeEnum | 1 Phone, 2 Email, 3 WhatsApp |
| products.product_type | ProductTypeEnum | 1 Standard, 2 Apparel, 3 Perishable, 4 Bulk |
| products.sale_unit | SaleUnitEnum | 1 Unit, 2 Kilogram, 3 Liter, 4 Meter |
| products.lifecycle | LifecycleEnum | 1 Active (em linha), 2 Discontinued (fora de linha) |
| products.abc_class, stock_policies.abc_class | AbcClassEnum | 1 A, 2 B, 3 C |
| calendar_events.scope | EventScopeEnum | 1 National, 2 Company |
| calendar_events.date_rule | DateRuleEnum | 1 Fixed, 2 Easter, 3 NthWeekday, 4 BlackFriday, 5 EasterOffset |
| stock_movements.type | MovementTypeEnum | 1 In, 2 Out |
| stock_movements.reason | MovementReasonEnum | 1 Opening, 2 Purchase, 3 Sale, 4 CustomerReturn, 5 SupplierReturn, 6 TransferIn, 7 TransferOut, 8 CountAdjustment, 9 Adjustment, 10 Breakage, 11 Expired, 12 Theft, 13 InternalUse |
| stock_movements.source_type | SourceTypeEnum | 1 Order, 2 PurchaseOrder, 3 Transfer, 4 InventoryCount, 5 Manual |
| orders.status | OrderStatusEnum | 1 Budget, 2 Paid, 3 Canceled, 4 Refunded, 5 Expired |
| orders.channel | OrderChannelEnum | 1 Counter, 2 Order |
| payments.method | PaymentMethodEnum | 1 Cash, 2 CreditCard, 3 DebitCard, 4 BankTransfer, 5 Pix |
| promotions.source | PromotionSourceEnum | 1 Manual, 2 AiRecommendation |
| purchase_orders.status | PurchaseStatusEnum | 1 Budget, 2 Pending, 3 Received, 4 Canceled |
| forecast_runs.trigger | ForecastTriggerEnum | 1 Manual, 2 Scheduled |
| forecast_runs.status | ForecastRunStatusEnum | 1 Running, 2 Completed, 3 CompletedWithoutAi, 4 Failed |
| forecast_ai_batches.status | AiBatchStatusEnum | 1 Pending, 2 Sent, 3 Completed, 4 Failed |
| forecast_recommendations.action | RecommendationActionEnum | 1 Buy, 2 Promote, 3 Hold, 4 Transfer |
| forecast_recommendations.priority | RecommendationPriorityEnum | 1 Low, 2 Medium, 3 High |
| forecast_recommendations.confidence | ForecastConfidenceEnum | 1 Low, 2 Medium, 3 High |
| forecast_recommendations.status | RecommendationStatusEnum | 1 Pending, 2 Applied, 3 Dismissed, 4 Expired |
| forecast_recommendations.lead_time_source | LeadTimeSourceEnum | 1 History, 2 ProductSupplier, 3 Supplier |
| forecast_recommendations.dismiss_reason_code | DismissReasonEnum | 1 BoughtElsewhere, 2 DisagreeQuantity, 3 WillDiscontinue, 4 Other |
| notifications.type | NotificationTypeEnum | 1 NewRecommendations, 2 LotExpiring, 3 LowStock |

Valores do enum que não são usados no escopo do TCC: `Budget`, `Refunded` e `Expired` em `orders.status` e `Order` em
`orders.channel` (orçamento e reembolso ficaram fora), `InventoryCount` em `source_type` e `CountAdjustment` em `reason`
(inventário fora), `User` em `users.role` (só Administrador, ADR 0004). Por isso os comentários no diagrama citam só os usados.

## Como estes diagramas foram montados (método reaproveitável)
1. **Extrair do banco, não do código nem da memória.** O banco com as migrations aplicadas é o que existe de fato.
   Duas consultas ao `information_schema` (colunas com tipo e nulidade; PK, FK e UNIQUE), salvas em [`esquema/`](esquema):
   ```bash
   docker exec -i <postgres> sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -AtF"|" -c "
     select table_name, column_name, data_type, is_nullable, coalesce(character_maximum_length::text,'"''"'),
            ordinal_position, coalesce(numeric_precision::text,'"''"'), coalesce(numeric_scale::text,'"''"')
     from information_schema.columns where table_schema=current_schema() and table_name<>'"'__EFMigrationsHistory'"'
     order by table_name, ordinal_position"' > esquema/colunas.txt
   ```
   A de chaves junta `table_constraints`, `key_column_usage` e `constraint_column_usage` (saída: tabela|coluna|referência|tipo).
2. **Gerar por script** ([`gerar_der.py`](gerar_der.py)), com o vocabulário do domínio em três dicionários:
   `NAMES` (nome em português de cada tabela), `VERBS` (verbo de cada FK) e `COMMENTS` (significado das colunas
   codificadas). O script **falha** se uma tabela ficar sem módulo ou sem nome, ou se uma FK ficar sem verbo, então
   uma migration nova não passa despercebida. A cardinalidade sai da nulidade da FK (`||` obrigatória, `|o` opcional).
3. **Recortar por módulo, até ~8 tabelas e ~12 ligações por figura.** Passou disso, dividir pelo fluxo (aqui, a
   previsão virou "análise" e "aplicação"). Tabela de outro módulo entra só com a chave, na cor do módulo dela.
   Quando a figura precisa das FKs de uma tabela de outro módulo, ela entra como **pivô** (só com essas colunas).
4. **Tirar o que não ensina:** colunas de auditoria e tamanhos de campo saem do desenho e vão para o texto.
5. **Verbo em toda ligação**, escrito para ler do pai para o filho.
6. **O diagrama geral não lista colunas:** com 82 FKs vira um emaranhado. O apêndice é um **mapa de módulos**
   (flowchart): caixas com as tabelas e setas com a contagem de FKs entre módulos, sem as FKs de autoria para `users`,
   que ligariam tudo a tudo.
7. **Dicionário de enums** no texto: colunas `smallint` não dizem nada sem os valores.
8. **Revisar olhando a imagem** e conferir uma figura contra o banco por amostragem.

### Truques de Mermaid específicos do DER
| Problema | Solução |
|--|--|
| Cor por entidade não funciona (`classDef` dá erro de sintaxe) | Usar o mermaid-cli 11.6 ou mais novo (aqui, 11.9.0) |
| Tipo `varchar(100)` quebra o parser | Tipo sem parênteses; o tamanho fica no esquema extraído |
| Nome da tabela em português com espaço | Alias: `stores["Loja (stores)"] { ... }` |
| Fonte pequena demais no PNG | `themeVariables: fontSize: 20px` no cabeçalho e `-s 2 -w 1800` na renderização |
| Ligação sem FK física | Linha tracejada: `clients ||..o{ addresses : "tem endereços"` |

## Como gerar de novo
Depois de uma migration nova: refazer a extração do passo 1 e, nesta pasta,
```bash
python3 gerar_der.py
for f in der-*.mmd; do
  docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/data" minlag/mermaid-cli:11.9.0 \
    -i "/data/$f" -o "/data/${f%.mmd}.png" -b white -s 2 -w 1800
done
```
