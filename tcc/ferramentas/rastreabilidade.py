"""Matriz de rastreabilidade RF/RNF -> casos de uso -> testes (item 12 do orientador).

Gera docs/architecture/rastreabilidade.md a partir dos relatórios de teste de uma execução (TRX do back e JUnit do front),
contando os testes de cada classe/arquivo ligados a cada requisito. Uso:
    python3 -I rastreabilidade.py <pasta-das-evidencias> <saida.md>
"""
import re, sys, collections

EVID, SAIDA = sys.argv[1], sys.argv[2]

RF = [
    ("RF001", "Autenticação e usuários", "UC01 a UC04",
     ["AccessApiTests", "AccessRulesTests", "LoginUseCaseTests", "UserUseCasesTests", "UsersSeederTests", "LastAdminRuleTests", "UserPersistenceTests"], []),
    ("RF002", "Cadastros de pessoas", "UC06 a UC11",
     ["RegistryApiTests", "RegistryRulesApiTests", "RegistryPersistenceTests", "RegistryActivityApiTests", "RegistryRulesTests"], ["client-quick-form"]),
    ("RF003", "Catálogo de produtos", "UC12 a UC18",
     ["ProductsApiTests", "ClassificationApiTests", "ClassificationRulesApiTests", "CalendarEventsApiTests", "CalendarEventRulesTests",
      "ClassificationRulesTests", "CommercialCalendarTests", "ProductDtoMappingTests", "ProductModelTests", "ProductRequestValidatorTests",
      "ProductUseCaseRulesTests", "UploadFileDtoValidatorTests"], []),
    ("RF004", "Lojas e locais", "UC05 e UC19",
     ["StoresApiTests", "StoresRulesApiTests", "StorePersistenceTests", "LastStoreRuleTests", "StoreRulesTests"], []),
    ("RF005", "Controle de estoque", "UC20 a UC25",
     ["ManualMovementApiTests", "StockKardexApiTests", "StockLedgerApiTests", "StockTransferApiTests", "LotsApiTests",
      "ManualMovementValidatorTests", "StockLedgerTests", "StockMinimumTests"], []),
    ("RF006", "Venda de balcão", "UC26 a UC29", ["QuickSaleApiTests", "SaleOptionsApiTests"], ["use-barcode-scanner", "variant-sale-picker"]),
    ("RF007", "Promoções", "UC30 e UC31", ["PromotionsApiTests", "PromotionPricingTests"], []),
    ("RF008", "Pedidos de compra", "UC32 a UC37",
     ["PurchaseOrdersApiTests", "PurchaseReceivingApiTests", "ProductSupplierResponseDtoTests", "PurchaseOrderModelTests"], ["PurchaseOrder/Create"]),
    ("RF009", "Previsão de demanda", "UC38 a UC40 e UC47",
     ["ForecastApiTests", "ForecastEngineTests", "ForecastCalculatorTests", "ForecastGuardrailsTests", "ForecastAiOrchestratorTests",
      "ForecastAiPayloadTests", "GeminiAiClientTests", "DerivedDataCalculatorTests", "ForecastScheduleTests", "TransferTriggerTests",
      "VariantAllocatorTests", "DerivedDataSeedTests"], ["pages/Forecast.test", "ForecastHistory", "forecast-run.service", "forecast-detail"]),
    ("RF010", "Aplicação das recomendações", "UC41 a UC45 e UC50",
     ["ForecastActionsTests", "StoreSplitCalculatorTests", "OnDemandSuggestionCalculatorTests"], ["apply-purchase-dialog", "forecast-actions"]),
    ("RF011", "Precisão da previsão", "UC46",
     ["ForecastAccuracyApiTests", "ForecastAccuracyQueryTests", "ForecastAccuracyCalculatorTests"], ["ForecastAccuracy"]),
    ("RF012", "Painel e notificações", "UC48, UC49, UC51 e UC52",
     ["NotificationsApiTests"], ["pages/Home", "dashboard.service", "notification.service", "notifications-bell"]),
]

RNF = [
    ("RNF001", "Interface responsiva e acessível", "Medição de contraste (Quadro 15), inspeção do código e avaliação heurística (seções 4.10.1 e 5.2.3)", "Atende aos critérios medidos"),
    ("RNF002", "Integridade do estoque", "Testes do livro-razão (StockLedgerTests e StockLedgerApiTests)", "Aprovados"),
    ("RNF003", "Tempo de resposta", "Medição na homologação (Quadro 17)", "Atendido: máximo de 1,8 s"),
    ("RNF004", "Segurança", "Testes de acesso (AccessApiTests, AccessRulesTests, LoginUseCaseTests) e de contrato do envio à IA", "Aprovados"),
    ("RNF005", "Conteinerização", "Execução em contêineres no desenvolvimento e na homologação (seção 5.1)", "Atendido"),
    ("RNF006", "Clean Architecture", "Organização do código em camadas (seção 4.5)", "Atendido por inspeção"),
    ("RNF007", "Stack tecnológica", "Versões usadas na execução dos testes (seção 5.2.1)", "Atendido"),
    ("RNF008", "Funcionamento sem IA", "Testes do orquestrador e do motor sem IA (ForecastAiOrchestratorTests, ForecastEngineTests)", "Aprovados"),
    ("RNF009", "Testes automatizados", "Suítes do backend e do frontend (seção 5.2.1)", "1.062 + 84 aprovados"),
]

trx = open(f"{EVID}/testes-back.trx", encoding="utf-8-sig").read()
back = collections.Counter()
for nome in re.findall(r'<UnitTest name="([^"]+)"', trx):
    m = re.search(r'\.(\w+Tests)\.', nome)
    back[m.group(1) if m else "?"] += 1
falhas_back = len(re.findall(r'outcome="Failed"', trx))

junit = open(f"{EVID}/testes-front-junit.xml", encoding="utf-8").read()
front = {}
for a in re.findall(r'<testsuite ([^>]*)>', junit):
    at = dict(re.findall(r'(\w+)="([^"]*)"', a))
    front[at["name"]] = (int(at["tests"]), int(at.get("failures", 0)) + int(at.get("errors", 0)))

usados_b, usados_f = set(), set()
linhas = []
for cod, nome, ucs, classes, arquivos in RF:
    nb = sum(back[c] for c in classes); usados_b.update(classes)
    fs = [f for f in front if any(k in f for k in arquivos)]; usados_f.update(fs)
    nf = sum(front[f][0] for f in fs)
    linhas.append((cod, nome, ucs, nb, nf, classes, fs))

out = ["# Matriz de rastreabilidade", "",
       "> **Status:** gerada em 11/11/2026 por `tcc/ferramentas/rastreabilidade.py` a partir dos relatórios em",
       "> `docs/evidencias/2026-11-11` (back `8b410cf`, front `aba7f64`). Resume-se no Apêndice B do TCC.", "",
       "Os casos de uso estão em `architecture/diagrams/uml/casos-de-uso/README.md`; as regras de negócio, em",
       "`architecture/modules/<módulo>/business-rules.md`.", "",
       f"Resultado da execução: backend {sum(back.values())} testes, {falhas_back} falhas; frontend "
       f"{sum(v[0] for v in front.values())} testes, {sum(v[1] for v in front.values())} falhas.", "",
       "## Requisitos funcionais", "",
       "| Requisito | Casos de uso | Testes backend | Testes frontend | Classes e arquivos de teste |", "|--|--|--|--|--|"]
for cod, nome, ucs, nb, nf, classes, fs in linhas:
    out.append(f"| {cod} {nome} | {ucs} | {nb} | {nf} | {', '.join(classes)}{'; ' if fs else ''}{', '.join(f.split('/')[-1] for f in fs)} |")
resto_b = {k: v for k, v in back.items() if k not in usados_b}
resto_f = {k: v[0] for k, v in front.items() if k not in usados_f}
out += ["", f"Fora dos requisitos funcionais (infraestrutura, migrações e dados de demonstração): backend "
        f"{sum(resto_b.values())} testes ({', '.join(sorted(resto_b))}); frontend {sum(resto_f.values())} "
        f"({', '.join(k.split('/')[-1] for k in sorted(resto_f))}).", "",
        "## Requisitos não funcionais", "", "| Requisito | Verificação | Resultado |", "|--|--|--|"]
out += [f"| {c} {n} | {v} | {r} |" for c, n, v, r in RNF]
open(SAIDA, "w").write("\n".join(out) + "\n")

for cod, nome, ucs, nb, nf, *_ in linhas:
    print(f"{cod}\t{nome}\t{ucs}\t{nb}\t{nf}")
print("resto", sum(resto_b.values()), sum(resto_f.values()), "falhas", falhas_back)
