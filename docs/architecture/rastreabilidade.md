# Matriz de rastreabilidade

> **Status:** gerada em 11/11/2026 por `tcc/ferramentas/rastreabilidade.py` a partir dos relatórios em
> `docs/evidencias/2026-11-11` (back `8b410cf`, front `aba7f64`). Resume-se no Apêndice B do TCC.

Os casos de uso estão em `architecture/diagrams/uml/casos-de-uso/README.md`; as regras de negócio, em
`architecture/modules/<módulo>/business-rules.md`.

Resultado da execução: backend 1062 testes, 0 falhas; frontend 84 testes, 0 falhas.

## Requisitos funcionais

| Requisito | Casos de uso | Testes backend | Testes frontend | Classes e arquivos de teste |
|--|--|--|--|--|
| RF001 Autenticação e usuários | UC01 a UC04 | 95 | 0 | AccessApiTests, AccessRulesTests, LoginUseCaseTests, UserUseCasesTests, UsersSeederTests, LastAdminRuleTests, UserPersistenceTests |
| RF002 Cadastros de pessoas | UC06 a UC11 | 137 | 2 | RegistryApiTests, RegistryRulesApiTests, RegistryPersistenceTests, RegistryActivityApiTests, RegistryRulesTests; client-quick-form.test.tsx |
| RF003 Catálogo de produtos | UC12 a UC18 | 399 | 0 | ProductsApiTests, ClassificationApiTests, ClassificationRulesApiTests, CalendarEventsApiTests, CalendarEventRulesTests, ClassificationRulesTests, CommercialCalendarTests, ProductDtoMappingTests, ProductModelTests, ProductRequestValidatorTests, ProductUseCaseRulesTests, UploadFileDtoValidatorTests |
| RF004 Lojas e locais | UC05 e UC19 | 36 | 0 | StoresApiTests, StoresRulesApiTests, StorePersistenceTests, LastStoreRuleTests, StoreRulesTests |
| RF005 Controle de estoque | UC20 a UC25 | 91 | 0 | ManualMovementApiTests, StockKardexApiTests, StockLedgerApiTests, StockTransferApiTests, LotsApiTests, ManualMovementValidatorTests, StockLedgerTests, StockMinimumTests |
| RF006 Venda de balcão | UC26 a UC29 | 17 | 12 | QuickSaleApiTests, SaleOptionsApiTests; use-barcode-scanner.test.ts, variant-sale-picker.test.tsx |
| RF007 Promoções | UC30 e UC31 | 10 | 0 | PromotionsApiTests, PromotionPricingTests |
| RF008 Pedidos de compra | UC32 a UC37 | 20 | 4 | PurchaseOrdersApiTests, PurchaseReceivingApiTests, ProductSupplierResponseDtoTests, PurchaseOrderModelTests; Create.test.tsx |
| RF009 Previsão de demanda | UC38 a UC40 e UC47 | 142 | 28 | ForecastApiTests, ForecastEngineTests, ForecastCalculatorTests, ForecastGuardrailsTests, ForecastAiOrchestratorTests, ForecastAiPayloadTests, GeminiAiClientTests, DerivedDataCalculatorTests, ForecastScheduleTests, TransferTriggerTests, VariantAllocatorTests, DerivedDataSeedTests; Forecast.test.tsx, ForecastHistory.test.tsx, forecast-run.service.test.ts, forecast-detail.test.tsx |
| RF010 Aplicação das recomendações | UC41 a UC45 e UC50 | 36 | 12 | ForecastActionsTests, StoreSplitCalculatorTests, OnDemandSuggestionCalculatorTests; apply-purchase-dialog.test.tsx, forecast-actions.test.tsx |
| RF011 Precisão da previsão | UC46 | 25 | 3 | ForecastAccuracyApiTests, ForecastAccuracyQueryTests, ForecastAccuracyCalculatorTests; ForecastAccuracy.test.tsx |
| RF012 Painel e notificações | UC48, UC49, UC51 e UC52 | 2 | 19 | NotificationsApiTests; Home.test.tsx, dashboard.service.test.ts, notification.service.test.ts, notifications-bell.test.tsx |

Fora dos requisitos funcionais (infraestrutura, migrações e dados de demonstração): backend 52 testes (DemoCatalogSeedTests, DemoCatalogTests, DemoHistorySeedTests, DemoPhotosSeedTests, DemoScenariosSeedTests, FilterExpressionBuilderTests, FilterHelperTests, MigrationsTests, ResultFactoryTests, SearchKeyTests, UseCaseBaseTests); frontend 4 (use-breadcrumb-path.test.tsx, use-index-search.test.ts).

## Requisitos não funcionais

| Requisito | Verificação | Resultado |
|--|--|--|
| RNF001 Interface responsiva e acessível | Medição de contraste (Quadro 15), inspeção do código e avaliação heurística (seções 4.10.1 e 5.2.3) | Atende aos critérios medidos |
| RNF002 Integridade do estoque | Testes do livro-razão (StockLedgerTests e StockLedgerApiTests) | Aprovados |
| RNF003 Tempo de resposta | Medição na homologação (Quadro 17) | Atendido: máximo de 1,8 s |
| RNF004 Segurança | Testes de acesso (AccessApiTests, AccessRulesTests, LoginUseCaseTests) e de contrato do envio à IA | Aprovados |
| RNF005 Conteinerização | Execução em contêineres no desenvolvimento e na homologação (seção 5.1) | Atendido |
| RNF006 Clean Architecture | Organização do código em camadas (seção 4.5) | Atendido por inspeção |
| RNF007 Stack tecnológica | Versões usadas na execução dos testes (seção 5.2.1) | Atendido |
| RNF008 Funcionamento sem IA | Testes do orquestrador e do motor sem IA (ForecastAiOrchestratorTests, ForecastEngineTests) | Aprovados |
| RNF009 Testes automatizados | Suítes do backend e do frontend (seção 5.2.1) | 1.062 + 84 aprovados |
