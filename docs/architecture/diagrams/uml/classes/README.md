# Diagramas de classes (modelo de domínio)

> **Status:** rascunho para o TCC, feito em 09/11/2026 a partir das entidades do domínio (`nextflow.Domain/Models`);
> aguarda revisão do Daniel. Feito em **PlantUML**, como **modelo de domínio** (diagrama de classes de análise):
> conceitos do negócio em português, atributos e operações de negócio, ligações com verbo. A versão fiel ao código
> (nomes em inglês, tipos C#, todas as classes) fica em [`codigo/`](codigo) como referência técnica.

## Figuras
| Figura sugerida | Arquivo |
|--|--|
| Camadas da arquitetura no fluxo da venda rápida | [classes-0-camadas.png](classes-0-camadas.png) |
| Modelo de domínio — Acesso e cadastros | [dominio-1-acesso-cadastros.png](dominio-1-acesso-cadastros.png) |
| Modelo de domínio — Catálogo de produtos | [dominio-2-catalogo.png](dominio-2-catalogo.png) |
| Modelo de domínio — Estoque | [dominio-3-estoque.png](dominio-3-estoque.png) |
| Modelo de domínio — Vendas e promoções | [dominio-4-vendas.png](dominio-4-vendas.png) |
| Modelo de domínio — Compras | [dominio-5-compras.png](dominio-5-compras.png) |
| Modelo de domínio — Previsão de demanda com IA | [dominio-6-previsao.png](dominio-6-previsao.png) |
| Modelo de domínio — Dados que alimentam a previsão | [dominio-7-dados-previsao.png](dominio-7-dados-previsao.png) |
| (Apêndice, opcional) Diagramas de classes de implementação | [`codigo/`](codigo) |

Legenda no Word: "Figura N – Diagrama de classes: modelo de domínio (Módulo). Fonte: Elaborado pelo autor (2026)."
A figura das camadas fica com os nomes do código de propósito: ali o assunto é a arquitetura.

## Como ler
- **Cada caixa é um conceito do negócio**, com o nome em português e a cor do módulo (a mesma do DER).
- **Atributos** com tipos simples: Texto, Inteiro, Decimal, Percentual, Data, DataHora, Lógico. `[0..1]` = opcional.
  Quando o valor é uma lista curta, ela aparece direto ("manual ou IA"); listas maiores viram uma enumeração.
- **Operações** são as ações do negócio que a entidade executa e que guardam as regras (ex.: `enviar()`, `receber()`,
  `aplicarCompra(pedido)`). O estado só muda por elas.
- **Ligações:** verbo, multiplicidade nas pontas (`1`, `0..1`, `*`, `1..*`); ◆ = **composição** (a parte só existe dentro do
  todo). Muitos-para-muitos aparece direto (Produto `*—*` Categoria), sem a tabela do meio do banco.
  **Classe de associação** (linha tracejada até a ligação): "Fornecedor do produto" guarda o que vale para o par.
- **Legenda de cada figura:** como ler e as regras de negócio principais do módulo, com o código da regra.
- Caixa só com o nome = conceito de outro módulo, detalhado na figura dele.

## Roteiro para a banca
1. **Estoque (figura 3):** o saldo é a soma das movimentações, que nunca mudam. É a decisão central do sistema.
2. **Vendas e Compras (4 e 5):** composição (a venda é dona dos itens e pagamentos) e o ciclo de vida do pedido de compra
   pelas operações `enviar()`, `receber()` e `cancelar()`.
3. **Previsão (6):** a análise gera recomendações; a IA só prioriza e explica; aplicar liga a recomendação ao que ela gerou.
4. **Dados derivados (7):** por que existem (desempenho e ruptura não confundir a sazonalidade).

## Conceito × classe no código
| Conceito (figura) | Classe no código | Conceito (figura) | Classe no código |
|--|--|--|--|
| Usuário | `User` | Loja | `Store` |
| Notificação | `Notification` | Local de estoque | `StockLocation` |
| Usuário × Loja | `UserStore` | Saldo | `StockBalance` |
| Cliente | `Client` | Lote | `Lot` |
| Fornecedor | `Supplier` | Movimentação (livro-razão) | `StockMovement` |
| Endereço | `Address` | Mínimo por local | `StockLocationMinimum` |
| Contato | `Contact` | Política de estoque | `StockPolicy` |
| Cidade, Estado, País | `City`, `State`, `Country` | Transferência, item | `StockTransfer`, `StockTransferItem` |
| Produto | `Product` | Venda, item, pagamento | `Order`, `OrderItem`, `Payment` |
| Variação do produto | `ProductVariant` | Promoção | `Promotion` |
| Atributo da grade, valor | `ProductAttribute`, `ProductAttributeValue` | Pedido de compra, item | `PurchaseOrder`, `PurchaseItem` |
| Variação × valor | `ProductVariantValue` | Análise de previsão | `ForecastRun` |
| Histórico de preço | `PriceHistory` | Lote enviado à IA | `ForecastAiBatch` |
| Categoria, Produto × Categoria | `Category`, `CategoryProduct` | Projeção mensal | `ForecastProjection` |
| Coleção | `Collection` | Recomendação | `ForecastRecommendation` |
| Evento do calendário, Produto × Evento | `CalendarEvent`, `ProductEvent` | Item da recomendação | `ForecastRecommendationItem` |
| Fornecedor do produto | `ProductSupplier` | Parte da loja na compra | `ForecastRecommendationStore` |
| Venda mensal do produto | `ProductSalesMonthly` | Recomendação × Pedido | `ForecastRecommendationPurchaseOrder` |
| Sazonalidade do produto | `ProductSeasonality` | Agendamento da previsão | `ForecastSettings` |
| Fotografia diária do estoque | `StockDailySnapshot` | | |

## Como estes diagramas foram montados (método reaproveitável)
1. **Escolher o nível certo para o leitor.** Primeiro gerei o diagrama a partir do código (está em `codigo/`): fiel, mas
   com cara de implementação (tipos C#, `dto`, `utcNow`, classes de junção, 13 figuras). Para um documento acadêmico, o
   esperado é o **modelo de domínio**: o negócio, não o código. Os dois são válidos; servem a leitores diferentes.
2. **Partir da versão de código como inventário**, para não esquecer atributo nem operação, e traduzir à mão:
   - nome do conceito e dos atributos em português; tipos simples;
   - cortar o que é técnico: chaves, auditoria, tempo de execução, provedor e modelo de IA, contadores, ordem de exibição;
   - operações com o verbo do negócio e parâmetros de negócio (sem `dto`, `utcNow`, ids);
   - tabela de junção sem atributos vira ligação muitos-para-muitos; com atributos vira **classe de associação**;
   - enum longo vira enumeração em português; enum de 2 ou 3 valores entra direto no tipo do atributo.
3. **Agrupar por assunto, não por tabela:** 7 figuras (a versão de código tinha 13).
4. **Legenda com "como ler" e as regras**, para a figura se explicar sozinha no Word e no slide.
5. **Tabela conceito × classe** no texto, para ligar o modelo ao código quando perguntarem.
6. **Revisar olhando a imagem.** Armadilha encontrada: em `enum`, valor com parênteses ("Transferência (entrada)")
   é lido como método e vai para baixo de uma linha divisória; escrever sem parênteses.

## Como gerar as imagens
```bash
docker run --rm -u "$(id -u):$(id -g)" -e JAVA_TOOL_OPTIONS="-Duser.home=/tmp -DPLANTUML_LIMIT_SIZE=8192" \
  -v "$PWD/..:/data" -w /data/classes plantuml/plantuml:1.2024.7 -tpng -charset UTF-8 dominio-*.puml classes-0-camadas.puml
```
(rodar dentro desta pasta)
