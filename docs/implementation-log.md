# Log de implementação — Nextflow (branch `feat/arquitetura-atrena`)

> Relatório fatia a fatia do `implementation-plan.md`. O Daniel valida o resultado final por este arquivo.
> Execução autônoma pedida por ele em 30/10/2026: um agente por módulo, um de testes e um validador como portão de qualidade.

## Decisões da Fase 0 (delegadas pelo Daniel em 29/10/2026)
1. `lastStoreId` sai do contrato: a última loja fica no localStorage do front.
2. Usuário inativo é checado a cada requisição, com 401.
3. Combos usam `GetOptionsUseCaseBase` no núcleo (busca, só ativos, até 20).
4. `/api/addresses` e `/api/contacts` com `ownerType` + `ownerId`, um principal por dono, exclusão física.
5. País, estado e cidade são só leitura, com seed do IBGE.
6. `user_stores`: criar loja vincula todos os Admins ativos; criar usuário vincula todas as lojas ativas.
7. Não se inativa o local padrão de uma loja.
8. A FK da recomendação para o documento gerado fica na recomendação (`applied_*_id`).

## Fase 0 — Fundação

### F0.1 Esqueleto
Solução .NET 10 com o núcleo do atrena (`ResultDto` com `FieldErrors`, bases de use case, filtros, UnitOfWork, middleware) e `GET /health`.
Build sem avisos; 18 testes. Anterior à rodada com validador.

### F0.2 Banco limpo
Migration inicial vazia, compose `nextflow-v2-development` separado do dev antigo (Postgres 5435, API 8081, storage 9010), appsettings por ambiente.
20 testes, incluindo migrations aplicadas do zero por Testcontainers. Anterior à rodada com validador.

### F0.3 Front base
`api.service` com envelope novo, `useApiForm` + `ConfirmWarningDialog`, enums em string, tokens do shadcn; enums antigos isolados em `legacy-enums.ts`.
Erro por campo comprovado na tela de login, junto da F0.4.

### F0.4 Acesso
- **Feito:** usuários, `/api/auth` (login, me, perfil, troca de senha), token de 8 h, senha forte, último acesso, bloqueio de inativar a si mesmo e o último Admin, checagem de inativo a cada requisição; telas T-AC1 a T-AC4.
- **Testes:** 115 aprovados, 0 falhas, 0 ignorados. Telas por Playwright em claro, escuro e mobile.
- **Validador:** reprovada na primeira rodada (6 correções, sem defeito funcional) e **aprovada** na revalidação de 30/10/2026: `dotnet format` limpo, build sem avisos; front com eslint, prettier e build limpos. Login e CRUD confirmados por requisição real. JSON quebrado devolve 400 e campo inconversível, 422.
- **Decisões:** RN-AC06..14 registradas em `access/business-rules.md`. Corrida do último Admin aceita como risco conhecido (porte de 4 a 15 funcionários; ADR 0010 não tem transação manual). Sem `Seed__Admin__Password`, a API não sobe fora de Development; o compose de staging exige `SEED_ADMIN_PASSWORD`.
- **Em aberto:**
  - contraste no tema escuro abaixo de AA (texto sobre `--primary` 4,01; botão destrutivo 2,77);
  - cadastro simultâneo com o mesmo e-mail deve virar 500 pelo índice único (lido no código, não reproduzido);
  - Home mostra toasts de 404 até o painel existir (F3.5).

### F0.5 Localidade e cadastros
- **Feito:** países, estados e cidades só leitura (seed IBGE: 2 países, 27 estados, 5.570 cidades), endereços e contatos polimórficos com CHECK, fornecedores e clientes, combos com `GetOptionsUseCaseBase`, cadastro rápido de cliente (API; botão entra na F2.4), filtro de aniversariantes; telas T-CD1 a T-CD4. Telas de CRUD de localidade removidas.
- **Testes:** 239 aprovados, 0 falhas, 0 ignorados. Telas por Playwright e pelo validador no navegador, com ViaCEP real.
- **Validador:** reprovada na primeira rodada (`Include` fora de `GetInclude()`, `mainPhone` trazendo telefone não principal, registros no guia) e **aprovada** na revalidação de 31/10/2026.
- **Decisões:** RN-CD06 (primeiro nasce principal; no máximo um; zero é aceito, excluir ou desmarcar não promove outro), RN-CD07..09, RN-CD10 (dono inativo não recebe nem altera endereço e contato). Riscos aceitos pelo porte: dois principais em requisições simultâneas e 500 em CPF/CNPJ duplicado simultâneo. Sufixo `XSummaryDto` registrado no guia.
- **Em aberto:** criar cliente e editar/excluir endereço pela tela só por Playwright do agente de testes, não pelo validador; busca sem acento não casa nome acentuado (registrado no contrato).

### F0.6 Lojas e locais
- **Feito:** `stores` ⇄ `stock_locations` (criar loja cria o local "Loja" como padrão de venda e recebimento no mesmo commit), `user_stores`, `/api/stores`, `/api/stock-locations`; tela T7 em `/settings/stores`; seletor de loja no topo (última loja no localStorage; some com 1 loja e 1 local).
- **Testes:** 275 aprovados, 0 falhas, 0 ignorados. Telas por Playwright em escuro e mobile 375.
- **Validador:** **aprovada** em 31/10/2026, na primeira rodada: `dotnet format` limpo, build sem avisos, front limpo; fluxo principal confirmado na tela, na API e no banco.
- **Decisões:** RN-CE35 a 37. Inativar loja é soft delete, a última ativa não sai, locais somem dos combos com a loja e voltam ao reativar (RN-CE36, a validar com o Daniel). FKs dos padrões em SQL `DEFERRABLE INITIALLY DEFERRED` na migration, fora do modelo do EF, protegidas por teste de persistência. `locationCount` novo em `CurrentUserStoreDto`. Corrida da última loja aceita como risco.
- **Em aberto:** criar local, trocar padrões e o estado sem seletor foram dirigidos pelo agente de testes, não pelo validador; `CurrentUserStoreDto` é montado em `UserStoreRepository.GetActiveStores` (observação do validador).

## Fase 0: concluída em 31/10/2026
275 testes verdes; F0.4, F0.5 e F0.6 aprovadas pelo validador. **Ponto de retomada: F1.1 Classificação.**

## Validação retroativa de F0.1, F0.2 e F0.3 (31/10/2026)
Reprovadas na rodada retroativa e corrigidas. O núcleo confere com o atrena e o ADR 0010, `/health` responde, o compose isolado e as migrations aplicam do zero.
- **Achado principal:** os `appsettings` estavam fora do git desde a F0.1. Em checkout limpo, 120 de 275 testes falhavam por falta de `JwtSettings:Key` e a API não gravava logs de aplicação. Corrigido: arquivos versionados (sem segredo de produção) e `AccessApiFixture` com a própria chave. Conferido em checkout limpo: **275 aprovados, 0 falhas**.
- **F0.3:** prettier em 9 arquivos corrigido; `OrderAction`, `AiBatchStatus`, `AbcClass`, `DismissReason` e `NotificationType` adicionados a `enums.ts`.
- **Doc:** `source_type` do `DOMAIN_LEVELS` alinhado ao contrato (`Transfer`, `Manual`).

## Fase 1 — Catálogo e estoque

### F1.1 Classificação
- **Feito:** `categories` (2 níveis validados no use case) e `collections`; telas T4 e T5 em dialog; telas antigas de categoria removidas.
- **Testes:** 319 aprovados, 0 falhas, 0 ignorados. Telas por Playwright em claro, escuro e mobile.
- **Validador:** reprovada na primeira rodada (`Include` fora de `GetInclude()`, DTOs agrupados, navegações sem `virtual`) e **aprovada** na revalidação de 31/10/2026.
- **Decisões:** RN-CE38 (nome único entre irmãs), RN-CE39 (categoria ativa tem pai ativo), RN-CE40 (coleção com nome único, datas opcionais e `is_active`), a validar com o Daniel. Riscos aceitos: neta em gravações simultâneas; `Doces`/`doces` simultâneos.
- **Em aberto:** "não inativa com produtos ativos sem confirmar" (T4) entra na F1.3; no combo de pai, ao editar filha, os outros pais só aparecem depois de digitar.

### F1.2 Calendário
- **Feito:** `calendar_events` com o calendário comercial portado, sete eventos nacionais no seed de todos os ambientes (idempotente, não sobrescreve antecedência nem status), `/api/calendar-events`, próxima data calculada só na API pelo relógio de negócio; tela T6 em `/calendar-events`.
- **Testes:** 459 aprovados, 0 falhas, 0 ignorados. Tela por Playwright em claro, escuro e mobile 375.
- **Validador:** reprovada na primeira rodada (trava do nacional sem teste para mês, dia da semana, ocorrência e deslocamento da Páscoa; relógio de negócio sem prova em POST, PUT e `GET /{id}`; `h-4 w-4` em vez de `size-4`) e **aprovada** na revalidação de 31/10/2026, com as mutações que antes sobreviviam agora derrubando testes.
- **Decisões:** RN-CE41 a RN-CE47, a validar com o Daniel. Colunas novas no DER: `weekday`, `nth`, `easter_offset_days`. 29/02 é recusado; ocorrência só de 1 a 4; `scope` nunca vem do cliente; nacional só muda antecedência e status; exclusão é soft delete nos dois escopos. Corrida de `Natal`/`natal` no nome único aceita como risco, igual a coleções.
- **A validar pelo Daniel, antecedência do seed:** Páscoa 42, Mães 21, Namorados 21, Pais 10 e Crianças 14 vêm do `DemoDemandModel` antigo. Natal 54 vem da janela de panetone e cesta, mas bombom, trufa e cesta de presente usam 24 no mesmo modelo. Black Friday 15 não tem base em dado. Pesa quando `lead_days` alimentar a previsão.
- **Em aberto:** `productCount` é zero até a F1.4; filtros de status e escopo aplicados só em desktop claro pela tela (nas demais, por API); seed em banco de dev vazio só nos testes de integração; sem `.env`, o front aponta para a porta 5145, e não para a 8081 do dev novo.

### F1.3 Produto e grade
- **Feito:** `products`, atributos e valores com `tempKey`, variações com a padrão oculta, `category_products`, imagem no S3 portado como `IFileStorage`; telas T1, T2 (campos por tipo) e T3 (só aba Variações). Fica fechada a pendência da F1.1: T4 pede confirmação ao inativar categoria com produtos, e `productCount` é real em T4 e T5. Telas antigas de pedido, compra, promoção e movimentação passaram a usar `legacy-*`.
- **Testes:** 659 aprovados, 0 falhas, 0 ignorados. Telas por Playwright em claro, escuro e mobile 375, com upload no Silo real.
- **Validador:** reprovada duas vezes. Primeira rodada: 8 defeitos (mutações sobreviventes, 500 com item nulo, `Include` fora de `GetInclude()`, navegação sem `!= null` em DTO, `CancellationToken.None` fora de rollback, `dark:` manual, estouro em 375 px, documentação divergente). Revalidação de 01/11/2026: um defeito, `GetFormOptions` sem teste do filtro e da ordem. Esse último foi corrigido com os dois testes que ele sugeriu e conferido pelo coordenador (as duas mutações agora derrubam teste; `dotnet format`, build e 659 testes verdes), **sem terceira rodada do validador**.
- **Decisões:** RN-CE48 a RN-CE57; RN-CE50, RN-CE52, RN-CE54 e RN-CE55 estão em "Perguntas em aberto". `PATCH /active` do contrato virou `DELETE` + `PATCH /reactivate` (ADR 0010). SKU e código de barras têm índice único em `lower(...)` além do índice exato, que o EF precisa para ordenar a gravação; reaproveitar o código de variação que sai só vale com a mesma grafia. Variação que sai do formulário é apagada de verdade enquanto não há saldo (ponto da F1.5 marcado).
- **Provisório, declarado no contrato:** `availableQuantity` 0, `hasLowStock` falso, custos e promoção nulos, todos fora da tela; T2 sem eventos, fornecedores, mínimos e cobertura. Preço efetivo = preço da variação até a F2.3.
- **Riscos aceitos:** corrida de SKU devolve 500 ao perdedor (a regra não fura: um único 201).
- **Em aberto:** 500 com caractere NUL em qualquer texto da API, inclusive em coleção e categoria (pede filtro único no `ApiController`); 500 com sinal Kelvin no SKU, sem corromper dado; upload acima de 30 MB derruba a conexão em vez de dar 422 (o front barra em 5 MB); os prints `14-produtos-lista*.png` e o do T3 são anteriores à troca de "A granel" para "Granel"; `silo-s3.md` ainda cita a porta 9000 no dev.
- **Ponto de retomada: F1.4 Preço e fornecedor.**

### F1.8 Kardex e mínimos
- **Decisões:** `stock_location_minimums` e `stock_policies` com id técnico e índice único (variação × local; classe), como as tabelas de vínculo da F1.3; `StockPolicyDto` ganhou `id` para o PUT usar a base de update. O mínimo por local cita a variação pela posição em `variants` (`variantIndex`), porque a variação nova não tem id. Kardex com use case próprio: o repositório do livro-razão não herda a base de CRUD (RN-CE14). Estoque baixo considera todo local ativo de loja ativa do recorte, sem saldo = 0; o filtro `lowStock` resolve os ids antes da paginação. Seed das políticas: A 15/7, B 30/5, C 45/3 (palpite, editável no T13). RN-CE06 obsoleta.
- **Fora:** lote no kardex (F1.7), número do documento na origem (cada documento, F2), classe ABC calculada (F3); a tela do kardex ainda não abre o drawer de ajuste (segue pela aba Estoque do T3).

### F1.11 Seed do catálogo
- **Decisões:** `DemoCatalogSeeder` (Order 50, `Seeders/Demo/`) só com `Seed:Demo:Enabled`, em duas etapas idempotentes: catálogo se não existe a categoria "Doces e Presentes"; saldo de abertura se nenhum local das lojas demo tem movimento, num documento `Manual`/`Opening` com custo pelo `IStockLedger` (dois commits porque o livro-razão lê as variações do banco). Lojas "Doce Encanto Centro" e "Doce Encanto Shopping", cada uma com "Loja" (venda) e "Depósito" (recebimento, não vendável). 42 produtos (5 com grade de tamanho ou sabor), 5 fornecedores com prazo e múltiplo, eventos Páscoa, Mães, Namorados e Natal; mínimo por local nos itens com mínimo padrão ≥ 20. Item de temporada com mínimo 0 (ovos, kits) abre sem saldo. A `AccessApiFixture` desliga o seed demo para os outros testes não verem o catálogo; a coleção do seed roda sem paralelismo (logger estático do Serilog).
- **Fora:** vendas e compras históricas (F2.9), lotes (F1.7), fotos.

### F2.1 Seletor de venda
- **Decisões:** `GET /api/sales/variant-options` com `storeId` obrigatório; sem `locationId` usa `stores.defaultSaleLocationId`; local inativo, não vendável ou de outra loja (e loja inexistente/inativa) é 422 no campo. Busca por nome, SKU ou código de barras em variações não removidas de produtos ativos (variação inativa e produto fora de linha entram, sinalizados); código de barras ou SKU exatos primeiro, `limit` 1–50. `VariantSaleOptionDto` ganhou `locationId` (local resolvido), para o aviso de falta excluir o local certo e a F2.4 saber de onde baixar. Disponível = físico no local até a F2.5. `GET /api/stock/availability` lista locais ativos de lojas ativas com disponível > 0, mesma loja do local excluído primeiro. Front: `VariantSalePicker` (Command + Popover, Enter do leitor com código exato escolhe direto, mesmo antes da busca responder) e `StockShortageDialog`; ainda sem tela que os use (entra na F2.4).
- **Fora:** `activePromotion` (F2.3), `nextLot` (F1.7), "Transferir agora" (F1.9) e "Cliente procurou" (F2.2): campos nulos e ações escondidas.

### F2.3 Promoções
- **Decisões:** `promotions` (produto ou variação, `discount_percent` numeric(5,2) com check 1–90, período com check, origem `Manual`, `forecast_recommendation_id` sem FK até a F3.4, `below_cost_confirmed`, autor). Status calculado na leitura pela data de negócio (Agendada, Vigente, Encerrada, Cancelada); cancelar = inativar por `POST /{id}/cancel`, só Agendada ou Vigente. Preço promocional = tabela × (1 − %/100), 2 casas, meio para cima, só no `IProductPricingService`, que agora lê o relógio de negócio e as promoções ativas de `Product.Promotions` (incluídas no `GetInclude()` de produtos e do seletor de venda). L-VD10 fechada pela recomendação: produto inteiro conflita com qualquer variação no período; duas variações diferentes, não (422 em `startDate`). Abaixo do custo médio: `confirm` e, confirmado, grava `belowCostConfirmed`; sem custo médio, sem aviso (decisão 0003). `SaleOptionPromotionDto` virou `PromotionSummaryDto` (mesmo JSON). `ProductVariant` passou a receber o produto no construtor, para o preço efetivo enxergar as promoções no grafo novo. Front: `/promotions` reescrita para a API nova (a tela e o dialog antigos saíram; o legado da previsão segue com `legacy-promotion.interface.ts`), dialog com prévia por variação, aba Promoções no T3 e selo "−X%" no T1 e nas variações.
- **Fora:** origem IA (F3.4), vendas no período (L-VD5), filtro "em promoção" e ordenação por preço efetivo no T1, promoção congelada no orçamento (F2.5).

### F2.8 Recebimento
- **Decisões:** `POST /purchase-orders/{id}/receive` só Pendente, todos os itens uma vez (senão 422 em `items`); uma entrada `Purchase` por item pelo `IStockLedger` (`SourceType = PurchaseOrder`); `product_variants.version` (int, token de concorrência, incrementado só em `ApplyInboundCost`) fecha a pendência da F1.5 sobre custo médio concorrente; `product_suppliers.last_cost` gravado só se o vínculo existe; `purchase_items.average_cost_after`, `purchase_orders.received_by` e `real_lead_time_days` (dia de negócio do recebimento − do envio). Migration `AddPurchaseReceiving`.
- **Fora:** lotes (F1.7: `lots` → 422, item com lote entra sem lote, como no ajuste manual), data retroativa (L-CP4), "receber com divergência" (L-CP1), média dos últimos 5 lead times (RN-CP06, bloco C).

### F2.9 Seed de 36 meses
- **Decisões:** `Seed:Demo:HistoryMonths` (36 no dev e no staging, 0 no padrão); `DemoHistorySeeder` (ordem 60) simula em memória com `Random(42)` e âncora `Seed:Demo:AnchorDate` ou hoje, e lança tudo pelo `IStockLedger` em ordem de data: abertura no dia 0 (substitui a da F1.11 quando o histórico está ligado), vendas Pago/Counter montadas como a venda rápida e pedidos de compra enviados e recebidos como na F2.8 (os que chegariam depois da âncora ficam Pendentes); datas pelos parâmetros dos modelos e `CreatedAt` ajustado no `ChangeTracker` (só o seed); commit por dia com o rastreador limpo. 36 meses levam ~3 min no startup (medido no teste de integração).
- **Fora:** promoções passadas, clientes, orçamentos, reembolsos, devolução ao fornecedor, transferências (compras do seed entram no salão; o depósito fica com a abertura), lotes, reajuste histórico de preço.

### F1.7 Lotes
- **Decisões:** tabela `lots` (variação, código até 40 normalizado em maiúsculas, validade; único por variação; imutável) com FK em `stock_balances` e `stock_movements` (migration AddLots). O `IStockLedger` resolve o lote antes de projetar: entrada de produto com lote exige lote, saída sem lote é repartida por FEFO (vencidos primeiro), lote em produto sem lote ou de outra variação → 422. Recebimento com `lots` por item somando a quantidade (uma entrada por lote; mesmo código e validade reaproveita o lote, outra validade → 422); ajuste com `lotId` ou `newLot`; aba Lotes `GET /api/products/{id}/lots?storeId` com dias para vencer e alerta de 30 dias; `GET /api/stock/lots/options`; `lotCode` no kardex e lotes no detalhe da compra. RN-CE55: troca de `tracksLots` com saldo → 422. Seed: alimentos com lote e 180 dias de vida útil (`ABERTURA` e `CyyMMdd`).
- **Fora:** escolha de lote na venda rápida (segue 422) e `nextLot` no seletor; alerta no painel (F3.5); transferência com lote; pular vencido na baixa.
- **A validar:** RN-CE15 (FEFO, era rascunho) e a janela de 30 dias.

### F3.1 Dados derivados
- **Decisões:** `product_sales_monthly`, `stock_daily_snapshots` e `product_seasonality` são derivadas e recriáveis (id técnico e índice único pela chave de negócio, como as tabelas da F1.8). `IDerivedDataService.RebuildAsync` lê vendas pagas (`GetPaidSaleLines`) e o livro-razão (`GetDeltasUntil`), calcula em memória pelo `DerivedDataCalculator` e regrava tudo num commit dentro de `IUnitOfWork.ExecuteInTransactionAsync` (exceção declarada ao ADR 0010, para não deixar as tabelas vazias se a gravação falhar); o DELETE em massa no repositório é exceção declarada a "repositório só registra". Saldo diário = soma acumulada das quantidades com sinal por variação × local, repetido nos dias sem movimento. Dia sem estoque do produto = soma do fechamento nos locais vendáveis ativos ≤ 0. Demanda perdida = dias sem estoque × média diária de venda dos dias com estoque (mês sem venda usa o último mês que vendeu). Índice sazonal só com 12 a 24 meses desde a primeira venda, limitado a [0,05; 5].
- **Fora:** endpoint de leitura, recálculo incremental e agendamento (F3.3), erro e exclusão de ruptura > 50% (F3.6), registro manual "cliente procurou" (F2.2, soma 0).
- **A validar:** dia sem estoque por soma dos locais vendáveis e fórmula da demanda perdida; custo de guardar 36 meses de saldo diário (medir no seed de 36 meses).

### F3.2 Motor portado + F3.7 Bug da temporada
- **Decisões:** cálculo puro em `Application/Forecast/` (`ForecastCalculator`, guardrails, templates, prompt, `ForecastHorizon`, `VariantAllocator`, `AbcClassifier`, `ForecastAiOrchestrator`) e leitura/gravação em `Application/Services/Forecast/` (`ForecastInputBuilder`, `ForecastEngine`, `IForecastEngine` no Domain). Entradas: `product_sales_monthly` e `product_seasonality` (F3.1; índice da categoria pela mesma fórmula), saldo e lotes do livro-razão, a chegar dos pedidos de compra Orçamento/Pendente, mínimo = soma dos mínimos efetivos das variações nos locais vendáveis. Horizonte automático `ceil(maior prazo ÷ 30) + 3`, teto 6; projeção até o horizonte e necessidade no prazo de cada produto (L-DF2). Cobertura alvo da política ABC substitui os 30 dias (RN-CE29), classe ABC recalculada e gravada; pedido mínimo, múltiplo e vida útil ajustam a quantidade. Rateio por variação pela venda de 24 meses (sem histórico: média; nenhum: igual, L-DF5) em `forecast_recommendation_items`. IA: `IAiClient` (Domain) e `GeminiAiClient` (HttpClient tipado, `Ai:*`, chave nunca em log), lotes sequenciais de 40 (`Forecast:AiBatchSize`), falha de lote cai para o cálculo, resumo em chamada final, sem chave `CompletedWithoutAi`. Commits: um por passo do progresso dos lotes e um final atômico (recomendações, projeções, expiração das pendentes, ABC, fechamento) em `ExecuteInTransactionAsync` (exceção ao ADR 0010, como na F3.1). Migration `AddForecastEngine` (5 tabelas; índice único parcial: um run `Running`). **F3.7:** produto de temporada fora da época (índice com pico >= 2 e média < 0,5 na janela de compra, ou, sem índice, vendas concentradas em 2 meses e nada nos 2 últimos) vira Manter, sem compra; fora de linha nunca recebe Comprar. O seed mostrou o defeito em 3 itens novos (DP-015, 044, 045: menos de 12 meses, índice plano) e o critério sem índice nasceu daí.
- **Fora:** endpoints, fila e agendamento (F3.3), aplicar ações (F3.4), Transferir (F3.4b), painel (F3.5), precisão (F3.6), front.
- **A validar:** cobertura alvo no lugar dos 30 dias (valores do seed A 15/7, B 30/5, C 45/3 deixam A com menos cobertura), limites da F3.7, mínimo somado por local, envio de nome e motivo de produtos à IA no resumo, estoque reservado fora do cálculo.

### Review da F3.2 + F3.7 (07/11/2026)
- Aprovada com ressalvas por agente validador (sem bloqueantes). Aplicadas no código: mínimo/múltiplo nos guardrails da IA, trava de rajada restrita a item novo sem índice, fechamento do run como `Failed` no cancelamento, reorganização de `IStockBalanceRepository` e `VariantShare`. Pendentes: teto de 90% no desconto da IA e os testes dos itens acima (lista em `slices/F3.2.md`). Execução interrompida por queda de energia e retomada; o agente de correções foi parado a pedido, e o estado foi commitado em `a0cdbaa`.

### Continuação do bloco C (08/11/2026, madrugada)
- **Branch:** `feat/bloco-c-previsao` do back, commits locais `e0c922a`, `ef54da0`, `fa2feff`, `4270254`, `518e9b3` sobre `a0cdbaa` (sem push).
- **F3.2/F3.7:** pendências da review fechadas com testes; desvio do ADR 0005 corrigido (a IA promovia sem gatilho do cálculo);
  previsão zerada na janela de compra vira "Sem ação" (Hold com motivo), proposta a confirmar.
- **F3.3:** fila em memória (`IForecastQueue`) + `ForecastRunWorker` (recalcula derivados e roda o motor), análise órfã vira `Failed` na
  subida, `ForecastScheduler` semanal (`forecast_settings`, migration `AddForecastSettings`), rotas de leitura (T-DF2, T-DF9, T-DF11).
- **F3.4:** detalhe e previsão do produto (T-DF3, T-DF5), Comprar (pedido em Orçamento por fornecedor, reaproveita `PurchaseOrderRules`),
  cancelar o pedido devolve a recomendação a Pendente, Promover (origem `AiRecommendation`, FK), Descartar com `DismissReason`
  (migration `AddForecastActions`).
- **F3.5:** rotas do painel (T-DF1), `notifications` por usuário ativo (migration `AddNotifications`), sino (T-DF12), aviso ao fim da
  análise e resumo diário (L-DF4).
- **Processo:** nas F3.3 a F3.5 os testes foram escritos junto com o código (não antes); sem review separada ainda.

### Bloco C: precisão, front e modelo reserva (08/11/2026)
- **Back (`feat/bloco-c-previsao`):** F3.6a–c (precisão: cálculo puro, projeção de referência, rotas T-DF10 e `accuracy` no T-DF5), F3.4c (422 do Aplicar Comprar nas linhas enviadas), tolerância ±15% (`b852dfc`) e modelo reserva da IA (`dcd1e3b`: prazo por tentativa, 2 tentativas por modelo, `Ai:FallbackModel` = `gemini-flash-lite-latest`). Suíte 1003/1003.
- **Regras aprovadas pelo Daniel:** RN-DF24, RN-DF25, RN-DF26.
- **Front (`feat/bloco-c-front`):** F3.8a–i. Limites aceitos: sem aviso de validade no Comprar (`maxByShelfLife` fora do DTO), sem "máximo permitido" no Promover (`maxDiscountPercent` fora do DTO), avisos de mínimo/múltiplo calculados no front porque o back aplica `ConfirmWarnings = true`.
- **Decisão:** previsão segue da empresa inteira; com loja no topo mostra o estoque da loja ao lado (`demand-forecast/decisions/0001`).
- **Em andamento à tarde:** `feat/filtro-loja`, `feat/historico-vendas`, `feat/venda-rapida-ajustes`, `feat/forecast-acoes` (estado em `slices/board.md`, seção "Em andamento").

### Merge na homolog e seed de fotos (08/11/2026, noite)
- Bloco C e as frentes da tarde (`filtro-loja`, `historico-vendas`, `venda-rapida-ajustes`, `forecast-acoes`) juntados na `homolog` dos dois repos; hashes em `slices/board.md`.
- `DemoPhotosSeeder` (ordem 80): fotos dos produtos demo baixadas do Unsplash e gravadas no Silo como o upload da tela; idempotente (só produto sem imagem) e tolerante a falha de rede (`LogWarning`). Testes com fonte fake, sem rede.
- Processo: worktrees por frente abandonados; uma branch por vez no checkout principal.

### Seed completo para testes (08/11/2026, noite)
- **Retomada do histórico:** cada dia do `DemoHistorySeeder` grava numa transação (`ExecuteInTransactionAsync`, exceção ao ADR 0010 restrita ao seed, a aprovar pelo Daniel); a âncora vai na nota da abertura e, se o startup cai no meio, o próximo refaz a simulação e continua do dia seguinte ao último gravado. Teste com queda simulada no 40º commit confere que o resultado é igual ao de um seed sem queda. Banco com abertura antiga (sem âncora na nota) não é retomado: precisa de `down -v`.
- **Vendedores:** 3 usuários demo (Admin, único perfil; senha aleatória, ninguém loga) vinculados às lojas; as vendas do histórico se repartem entre eles e o Admin por peso e por loja. Só com o histórico ligado.
- **Coleções:** Páscoa, Natal e Presentes Românticos, ligadas aos produtos na criação do catálogo.
- **`DemoScenariosSeeder` (ordem 65, só com histórico):** promoções vigente (produto e variação), agendada, encerrada e cancelada; pedidos de compra em orçamento, pendente atrasado e cancelado; um recebido ontem com lotes vencendo em 12 e 25 dias, pelo `IStockLedger`. Idempotente pela marca `(cenário demo)` no motivo ou na nota.
- **Fora:** venda cancelada ou reembolsada (o reembolso, F2.6, não existe na API).
- A promoção "encerrada" fica no passado sem preço promocional nas vendas do histórico daquele período (a previsão só usa a promoção vigente).

### Ajustes de tela: vendas e compras (08/11/2026, noite)
- **Back:** `WhereEnumEquals` aceita lista separada por vírgula (vira "está entre"); antes, `Budget,Pending` virava a soma dos valores (outro status). Vale para todos os filtros de status. 4 testes unitários (`FilterExpressionBuilderTests`).
- **Front (`feat/ajustes-vendas-compras`):** cantos do `Command` herdam o raio do popover (o search select vazava); detalhe da venda com cliente e vendedor em blocos, desconto em vermelho, pagamentos em verde com ícone e total em destaque; no histórico o nº abre o detalhe e a coluna Ações saiu; pedidos de compra com filtro de status múltiplo na barra (abre em Orçamento + Pendente), painel com fornecedor, período e "só atrasados", e a ação Receber na linha.
- **Baixa por lote:** a aba Lotes do produto ganhou "Dar baixa" por linha, que abre o ajuste manual (T9) já com variação, local, lote, saldo e motivo ("Vencido" se venceu, senão "Ajuste"). Sem mudança na API: o `POST /api/stock-movements/manual` já aceitava `lotId`.
- **Venda rápida repaginada:** duas colunas no desktop (carrinho à esquerda; cliente, pagamento e resumo fixos à direita), quantidade com − e +, desconto e valores com "R$", forma de pagamento em botões com ícone, "Dividir" para mais de uma forma, descontos em vermelho, total na cor da marca e faixa de falta pagar/troco. O resumo deixou de ser `sticky bottom`, que cobria o card de pagamento.
- **Achado no seed:** o saldo de abertura do depósito nunca sai (as vendas baixam só do salão e o seed não transfere), então todo lote "ABERTURA" no depósito aparece vencido. Fica para decidir: transferir do depósito no histórico ou abrir o depósito sem saldo.
- **Leitor sem Enter:** no seletor de venda, quando a busca responde e o termo é exatamente o SKU ou o código de barras de uma única opção, ela entra no carrinho sozinha. Efeito colateral aceito: quem digita à mão um SKU que é prefixo de outro (ex.: `DOC-001` e `DOC-0010`) e para de digitar leva o primeiro. 2 testes novos no `variant-sale-picker.test.tsx`.
- **Compras do cliente:** o nº da venda abre o mesmo detalhe do histórico (`components/app/sale-detail-dialog.tsx`, extraído da tela de histórico).
- **Mobile:** o card genérico do `DataTable` acha a coluna de ações pelo id `actions` (antes pegava a última, e no histórico de vendas sem ações o vendedor virava "ação") e mostra rótulo à esquerda e valor à direita; categorias em card por categoria com as subcategorias dentro; produto com foto, preço efetivo e disponível lado a lado, detalhes em duas colunas, e variações e lotes em card no celular. Venda rápida: rótulos curtos nos botões de pagamento ("Transferência") e card "Resumo" com cabeçalho.
- **Mobile, segunda rodada:** abas das telas de detalhe em grade de 3 no celular (sem rolagem horizontal); `meta.hideOnMobile` e `meta.label` nas colunas do `DataTable` (produtos sem tipo, categoria e variações no card; promoções sem origem e autor; movimentações com rótulo em lote, quantidade, custo e saldo); produto com estoque por local, fornecedores e preços em card; lojas (locais em linhas) e política de estoque em card.
- **Margem no topo do produto:** faixa das margens que a API já devolve por variação ativa (`marginPercent` = preço efetivo − custo médio, sobre o preço), em verde, ou vermelho se alguma é negativa; no celular fica ao lado do preço.
- **Leitor fora da busca (venda rápida):** `useBarcodeScanner` escuta o teclado da página; sequência de 4+ caracteres com menos de 50 ms entre eles, terminando em Enter (ou parando por 80 ms), vira leitura e vai para o seletor (`ref.scan`), e o Enter não aciona o botão focado. Dentro de um campo de texto não intercepta. A busca abre focada e o foco volta para ela depois de pagamento, quantidade, remover item e cadastro de cliente; leitura na tela de "venda concluída" abre a nova venda já com o item. 5 testes do hook.
- **Promoções:** `PUT /api/promotions/{id}` edita só a agendada (`UpdatePromotionUseCase`, 2 testes de integração); no front, Editar (o mesmo dialog, com o produto fixo) e Visualizar (dados gravados e, pela prévia, tabela → promoção, custo médio e margem de hoje por variação), na tela e na aba do produto.
- **Pedido de compra (criar e editar):** layout da venda rápida, com itens em linhas à esquerda e fornecedor/entrega, observação e resumo (itens, prazo e total salvo, sem somar no front) fixos à direita.
- **Seed, depósito:** só o que não vence fica no depósito; alimento abre todo no salão e tem mínimo zero no depósito (`DemoCatalog.KeepsInDeposit`). Antes o lote "ABERTURA" do depósito vencia parado. Teste `Should_KeepPerishablesOutOfDeposit_When_HistorySeeded`.
- **Visualizar em coleções e calendário:** o nome abre o detalhe (`onRowOpen`) e o menu ganhou "Visualizar"; os dois listam os produtos ativos ligados (`LinkedProductsList`, filtros `collectionId` e o novo `eventId` na listagem de produtos, teste `Should_ListOnlyLinkedProducts_When_FilteringByEvent`). Venda rápida: "Ver venda" na tela de venda concluída, com o mesmo detalhe do histórico.
- **Pedido de compra, local de entrega zerado:** o local padrão chegava antes da lista de locais e o `Select` do Radix chamava `onValueChange("")`, zerando o campo travado; "Adicionar item" nunca liberava. O formulário ignora o valor vazio. Busca de itens inline (`PurchaseItemPicker`) no estilo da venda rápida: foto, SKU, código de barras e custo médio (campos novos em `PurchaseVariantOptionDto`), código exato entra sozinho e "Todos os produtos" num interruptor.
- **Previsão:** "Promover selecionados" (`BulkPromoteDialog`, desconto e dias sugeridos por linha, uma chamada por recomendação, erro na linha) e "Descartar selecionados" (o dialog de descartar aceita várias com o mesmo motivo).
- **Painel, "ver mais":** `limit` (5 a 200) em `dashboard/low-stock` e `dashboard/expiring-lots`; os itens trazem ids (produto, variação, lote, local) e a recomendação pendente do produto (`recommendationId`, `recommendationAction`). Dialogs com ações: estoque baixo (comprar com a IA, novo pedido), lotes (promover com a IA, promover, dar baixa na aba Lotes) e próximas datas (produtos ligados ao evento). Teste `Should_ListMoreItemsWithPendingRecommendation_When_DashboardAsksForMore`.
- **Cartões novos:** `F3.9.md` (comprar dividido por loja, RN-DF27/28) e `F3.4b.md` (Transferir completo, RN-DF16 detalhado, RN-DF29, RN-CE62), aguardando aprovação.
- **F3.9 feita:** `StoreSplitCalculator` (puro, 5 testes), `GET .../store-split`, tabela `forecast_recommendation_purchase_orders` (migration `AddRecommendationPurchaseOrders`, preenche os pedidos já aplicados), cancelamento só volta a recomendação a Pendente sem pedido aberto, e "Dividir entre lojas" no dialog de comprar.
- **F3.4b feita (3 partes):** transferência de estoque (`StockTransfer` + itens, `IStockTransferService`, `IStockLedger.PostResolved` para a entrada repetir os lotes do FEFO, sem custo), gatilho `TransferTrigger` no motor depois dos guardrails, aplicar transferir e o cenário de seed. Migration `AddStockTransfers` (tabelas e `applied_transfer_id`, `transfer_from_location_id`, `transfer_to_location_id` na recomendação).
- **Pedidos do Daniel (08/11/2026, retomada):** divisão por loja no front (coluna Sugestão com a parte de cada loja, seção "Divisão por loja" no detalhe, comprar abre dividido quando `storeSplit` tem 2+ lojas e não exige local do grupo se todos os itens estão divididos; loja dividida sem local de recebimento padrão vira erro na linha); "Promover selecionados" virou a tela `/forecast/promote?ids=…` (`BulkPromoteForm`, recarrega pelos ids se a página for aberta direto); "ver mais" do painel virou `/dashboard/low-stock` e `/dashboard/expiring-lots`, com `storeId`/`storeName` nos itens (`LowStockItemDto`, `ExpiringLotItemDto`) e cada ação trocando a loja do topo antes de abrir. Teste novo do comprar ("abre já dividido"); front 81/81.
- **F3.10, IA na hora no painel (08/11/2026, noite, sem commit):** `GET /api/forecasts/suggestions/purchase` e `/promotion` (RN-DF30, a aprovar); todo item de estoque baixo tem "Comprar com a IA" e todo lote vencendo "Promover com a IA"; "Novo pedido de compra" abre o pedido com produto, fornecedor e quantidade calculada (`?productId&variantId&quantity`, motivo no topo); a promoção abre com variação, desconto, período e motivo. Breadcrumb com nomes para todas as rotas (`dashboard` some, `sales` sem link). Back: testes novos 9/9 (27/27 com os vizinhos); front 84/84.
- **Prints para o TCC (08/11/2026, noite, sem commit):** `nextflow-front/scripts/screenshots.mjs` (`npm run screenshots`, Playwright 1.56.1 como dependência de dev) gera 86 prints em `docs/screenshots/` (claro, escuro, celular) com relatório de erros por tela (nenhum). Bugs achados e corrigidos: unidade crua ("324 Unit") na previsão, no card do painel e nos dialogs de comprar e transferir (helper `unitShort`); botões "Filtros" e "Novo" das listagens sem texto no celular (faixa larga só com ícone); trajeto do "Transferir" quebrando em 6 linhas na coluna Sugestão. Front 84/84, build e lint ok.
- **Diagramas do TCC (09/11/2026):** refeitos do código e do banco atuais em `architecture/diagrams/uml/` (índice no README): casos de uso em PlantUML (8 figuras, UC01–UC52), DER em Mermaid (11 por módulo + mapa no apêndice, gerado por `der/gerar_der.py`), classes em PlantUML como modelo de domínio (7 + camadas; versão de código em `classes/codigo/`), sequência em Mermaid (7 fluxos). Ferramenta escolhida por tipo depois de comparar exemplos; cada pasta com "como ler", roteiro da banca e método.
