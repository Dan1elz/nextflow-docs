# Handoff — Nextflow (estado em 08/11/2026, madrugada)

> **Comece pela seção 0.5** (estado atual, sem commit, e o que o Daniel pediu por último). As seções 0 a 0.4 são histórico.
> Atualizado em 07/11 à noite (seção 0). Para continuar o trabalho de outro PC sem ajuda. Conferido contra o `git log` da `homolog` dos dois repos e contra
> os arquivos de setup reais. Detalhe de cada fatia: `slices/board.md` e os cartões `slices/F*.md`.

## 0. Atualização de 07/11/2026 (noite): bloco C em andamento
> Escrita ao fim da sessão de trabalho de 07/11; o resto do documento descreve o estado da manhã.

**O que foi feito hoje, além do handoff original**
- **Redesign do front** (visual estilo Apple, animações com `motion`, sidebar que expande no hover, logo só com o "n", dashboard sem cards): branch `feat/redesign-frontend` do front,
  commits `708c3bc` e `ecb8700`, **sem push**. Base: `homolog` (`c442a77`).
- **F3.1 Dados derivados** e **F3.2 Motor portado + F3.7**: no back, branch `feat/bloco-c-previsao`, commit `a0cdbaa` (sem push), saindo de `homolog` (`be6e911`).
  Cartões em `slices/F3.1.md` e `slices/F3.2.md`. Suíte: 936 testes verdes na entrega da F3.2; 93 unitários de previsão verdes depois das correções parciais.
- **Front, enums da F3.2**: branch `feat/bloco-c-previsao` do front, commit `0617ca0` (só `src/types/enums.ts`, `TLeadTimeSource`), saindo de `homolog`. **Não está na branch do redesign**: ao juntar as duas, é um merge trivial.
- **Docs**: branch `docs/bloco-c-previsao` (cartões F3.1 e F3.2, quadro, log, contrato e este handoff).

**Estado das fatias do bloco C**
| Fatia | Estado |
|--|--|
| F3.1 Dados derivados | Feita, review em duas rodadas (aprovada com ressalvas, corrigidas) |
| F3.2 + F3.7 Motor portado | Entregue; review aprovada com ressalvas, **correções parciais** (tabela em `slices/F3.2.md`, seção "Review") |
| F3.3 Análise em segundo plano | A fazer. Pré-requisito: chamar `IDerivedDataService.RebuildAsync` antes de `IForecastEngine.RunAsync`; mover a consulta do `ForecastInputBuilder` para repositório (`AsSplitQuery`) |
| F3.4 Ações (Comprar, Promover, Manter, Descartar) | A fazer |
| F3.5 Painel e notificações | A fazer. É o que enche o dashboard (`/api/dashboard/stats`) e o card de recomendações; hoje essas telas dão 404 na `homolog` |
| Front das telas T-DF | A fazer, depois das APIs |

**Pendências desta noite (para retomar)**
1. Terminar as correções da review da F3.2: teto de 90% no desconto da IA; testes de guardrails (mínimo/múltiplo), do cancelamento/`Failed`/índice único de run `Running`, do contraexemplo da trava de rajada e testes diretos do `ForecastInputBuilder`. Rodar a suíte completa depois.
2. Decisões para o Daniel: cobertura alvo da política ABC no lugar dos 30 dias fixos (e os valores A 15/B 30/C 45 do seed), limites da trava da F3.7, dia sem estoque do produto e fórmula da demanda perdida (F3.1), dados enviados à IA (custo médio e preço), precedência mínimo/múltiplo × vida útil.
3. Medir o tempo do seed de 36 meses com os dados derivados (a F3.1 acrescenta o recálculo no startup).
4. Revisão visual do redesign pelo Daniel; depois juntar `feat/redesign-frontend` e `feat/bloco-c-previsao` do front na `homolog`.

**Encerramento da sessão de 07/11 e ponto de retomada**
- A sessão foi encerrada a pedido do usuário, com a meta "fazer a etapa 3 inteira" **não concluída**: F3.3, F3.4 e F3.5 não foram começadas e a F3.2 tem correções pendentes.
- Tudo o que existe está commitado e sem push: back `a0cdbaa` (`feat/bloco-c-previsao`), front `0617ca0` (`feat/bloco-c-previsao`) e `ecb8700` (`feat/redesign-frontend`), docs `docs/bloco-c-previsao`.
- **Retomar por aqui:** (1) fechar as pendências da review da F3.2 (lista na seção "Review" de `slices/F3.2.md`) e rodar a suíte completa; (2) F3.3, com o pré-requisito de chamar `IDerivedDataService.RebuildAsync` antes de `IForecastEngine.RunAsync`; (3) F3.4; (4) F3.5; (5) front das telas T-DF. Uma fatia por vez, com agente validador do diff a cada fatia (o processo usado hoje).

**Exceções declaradas a regras da casa (para o Daniel aprovar)**
- `IUnitOfWork.ExecuteInTransactionAsync` (F3.1 e F3.2): ADR 0010 diz "sem transação manual"; usada só no recálculo dos dados derivados e no commit final do motor.
- DELETE em massa nos repositórios das tabelas derivadas (`DeleteAllAsync`): exceção a "repositório só registra"; as tabelas são recriáveis.

**Como rodar sem instalar o SDK no Windows (container)**
O host não precisa de .NET: use o container da imagem `nextflow-v2-backend:development` (SDK 10) com a solução montada e volumes próprios para `bin`/`obj`
(para não colidir com o `dotnet watch` da API). O script usado foi um `.f31-dotnet.sh` **local, fora do git** (`.git/info/exclude`), que monta
`-v <repo>:/src`, `-v f31_<projeto>_bin:/src/<projeto>/bin` e `..._obj` para cada projeto, `-v f31_nuget:/root/.nuget/packages`, `-v f31_tools:/root/.dotnet/tools`,
`-v //var/run/docker.sock:/var/run/docker.sock`, `TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal` e `TESTCONTAINERS_RYUK_DISABLED=true`, e roda `dotnet "$@"`.
Exemplos: `build nextflow-erp.sln -warnaserror`, `test nextflow.Tests --no-build --filter "FullyQualifiedName~Forecast"`, `format nextflow-erp.sln --verify-no-changes`,
`ef migrations add <Nome> --project nextflow.Infrastructure --startup-project nextflow` (instalar antes: `dotnet tool install --global dotnet-ef`). Só um comando dotnet por vez.
Com o Ryuk desligado, uma execução de teste interrompida deixa um container `postgres:17-alpine` parado: apague à mão. `dotnet format` acusa 4 erros antigos de whitespace em
`ProductUseCases.cs` e `StockAvailabilityUseCases.cs`.

**Ambiente local de hoje**: Docker Desktop + WSL2 no Windows; compose de dev `nextflow-v2-development` (Postgres 5435, API 8081, storage 9010), front por `npm run dev` (5173, `.env` com `VITE_API_URL=http://localhost:8081`).
Login de dev: `admin@nextflow.com` (senha `DevelopmentPassword` em `UsersSeeder.cs`). O seed de 36 meses leva alguns minutos no primeiro startup e agora também roda o recálculo dos dados derivados.

## 0.1 Atualização de 08/11/2026 (madrugada): bloco C concluído no back
- Retomado da branch do rodr1go22: correções e testes da review da F3.2, desvio do ADR 0005 corrigido (IA promovia sem gatilho),
  previsão zerada vira "Sem ação" (a confirmar), e F3.3, F3.4 e F3.5 implementadas. Commits locais na `feat/bloco-c-previsao` do back:
  `e0c922a`, `ef54da0`, `fa2feff`, `4270254`, `518e9b3` (sem push). Cartões `slices/F3.3.md`, `F3.4.md`, `F3.5.md`.
- Três migrations novas depois de `AddForecastEngine`: `AddForecastSettings`, `AddForecastActions`, `AddNotifications`.
- Falta: review das fatias (F3.4 densa), front das telas T-DF (o painel do front chama `/api/dashboard/stats`, que não existe; as rotas
  são as do contrato T-DF1), QA do bloco C e as decisões listadas nos cartões.

## 0.2 Atualização de 08/11/2026 (madrugada, depois da review)
- Review pelo padrão das F3.1 a F3.5 e F3.7 concluída: commit `d27ae54` na `feat/bloco-c-previsao` do back, 969/969 testes verdes,
  `dotnet format` limpo. Tudo local, **sem push**. O repo de trabalho é `~/Projetos/nextflow/nextflow` no WSL (as cópias
  `nextflow-blococ` e `nextflow-docs-blococ` foram só para não mexer na `homolog` durante o trabalho).
- Regras novas registradas (a confirmar com o Daniel): **RN-DF24** previsão zerada na janela de compra vira "Sem ação" (Hold com
  motivo) e **RN-DF25** a IA não promove sem gatilho do cálculo.
- Pendências: enum `TLeadTimeSource` ausente no `enums.ts` do front do WSL (F3.8a); índice do 422 no Aplicar Comprar quando a mesma
  variação vem em duas linhas (F3.4c).
- **O que falta do bloco C**, em fatias mínimas com aceite e testes: `slices/bloco-c-restante.md`. F3.6a (cálculo puro da precisão) feita, em review; próxima: F3.6b.
- **Ao aprovar o bloco:** merge de `feat/bloco-c-previsao` na `homolog` (back e, quando houver, front) e de `docs/bloco-c-previsao` na
  `main` dos docs. Push só quando o Daniel pedir.

## 0.3 Atualização de 08/11/2026 (tarde): bloco C completo, front incluso; frentes novas em andamento

**Feito e commitado (local, sem push)**
- **Back do bloco C completo** na `feat/bloco-c-previsao` (`~/Projetos/nextflow/nextflow`): F3.6a–c (precisão, `d0f9526`, `9bd4812`,
  `a8ee2e2`), F3.4c (`a106162`), tolerância de acerto **±15%** (`b852dfc`, era ±20%) e o **modelo reserva da IA** (`dcd1e3b`). Suíte 1003/1003.
- **Regras aprovadas pelo Daniel em 08/11:** RN-DF24 (previsão zerada na janela de compra vira "Sem ação"), RN-DF25 (IA não promove sem
  gatilho do cálculo) e RN-DF26 (dentro da tolerância com MAPE ≤ 15%; viés só acima de ±5%; mês com mais de 50% dos dias sem estoque fora).
- **Front do bloco C completo** (F3.8a–i) na `feat/bloco-c-front` (`~/Projetos/nextflow/nextflow-front`, último `167d07b`), saindo da
  `homolog` com o redesign: painel, sino, `/forecast`, detalhe em Sheet lateral e aba Previsão do produto, Comprar, Promover e Descartar,
  histórico, agendamento e `/forecast/accuracy`. Linhas e hashes em `slices/board.md`; o que ficou de fora de cada tela em `slices/bloco-c-restante.md`.
- **Modelo reserva:** o `gemini-flash-latest` deu 503 "high demand" e prendeu a conexão por até 141 s, então as análises saíam "Concluída
  sem IA". Agora o prazo é por tentativa, 2 tentativas por modelo, e cai para `Ai:FallbackModel` (`AI_FALLBACK_MODEL`, padrão
  `gemini-flash-lite-latest`). Detalhe em `architecture/integrations/gemini.md`.
- **`.env` do dev** (`~/Projetos/nextflow/nextflow/.env`, fora do git, chmod 600): só `AI_PROVIDER`, `AI_API_KEY` e
  `AI_MODEL=gemini-flash-latest`; o resto segue os padrões do compose. Sugestão em aberto: trocar `AI_MODEL` para o lite no dev
  (análise de ~15 s em vez de ~3,5 min enquanto o flash-latest estiver sobrecarregado).

**Em andamento (no fim da tarde de 08/11)**
Cada frente é uma branch local com git worktree no WSL; back sai da `feat/bloco-c-previsao`, front da `feat/bloco-c-front`. Tabela
completa (pastas, commits, o que está sem commit) em `slices/board.md`, seção "Em andamento".
- **`feat/filtro-loja`**: a loja do topo filtra painel, listas e o novo pedido de compra (que passa a exigir loja). Na previsão, a análise
  segue **da empresa inteira**; com loja no topo, a lista, o detalhe e o card do painel mostram o saldo e o "a caminho" da loja ao lado do total
  (`demand-forecast/decisions/0001-previsao-da-empresa-com-estoque-da-loja.md`). Front commitado; **back sem commit**.
- **`feat/historico-vendas`**: botão único Visualizar e filtros de cliente, vendedor, produto e faixa de valor (`GET /api/orders`).
  Commitado nos dois repos. Conflito pequeno previsto com a `feat/filtro-loja` em `sales-history.provider.tsx`.
- **`feat/venda-rapida-ajustes`**: leitor com Enter direto e aviso quando não acha, e-mail opcional no cadastro rápido de cliente, rodapé
  novo, sem o botão "Atualizar preços". Front commitado; **back sem commit**.
- **`feat/forecast-acoes`** (só front): ajustes da lista da previsão; branch criada, sem mudança ainda.
- **F3.4b Transferir**: opcional, só investigação.

**Backlog do Daniel (sem cartão):** filtros em todas as listagens; ver vendas e pedidos de compra pelo cliente e pelo fornecedor;
mobile quebrado; "ver mais" no painel; melhorias em pedidos de compra.

**Retomar por aqui**
1. Fechar as frentes em andamento (commitar o back de `feat/filtro-loja` e `feat/venda-rapida-ajustes`, rodar suíte e `eslint src`).
2. QA do Daniel: telas do bloco C e as frentes da tarde.
3. Com a aprovação, juntar na `homolog` na ordem do `slices/board.md` (bloco C primeiro) e os docs na `main`. Push só quando ele pedir.
4. Depois, o backlog acima (cada item vira cartão antes do código).

## 0.6 Atualização de 08/11/2026 (noite): pedidos fechados e tudo na homolog
- **Commits do back** (`feat/seed-completo`, cada um compila sozinho): `2f5e513` filtros (status em lista, `eventId`), `97a70e7`
  promoção (PUT), `d9c9a76` previsão (painel "ver mais", F3.9 + divisão por loja gravada pela análise, F3.4b, busca de itens da
  compra; migrations `AddRecommendationPurchaseOrders` → `AddStockTransfers` → `AddRecommendationStores`), `688b9ff` seed (depende da
  F3.4b). Merge na `homolog` `8cfa41a`. **Front:** `0b4c779` em `feat/ajustes-vendas-compras`, merge `bda3a20`.
- **Testes:** back 1045/1046 na suíte completa (a divisão por loja e `Should_SplitBuyAcrossStores_When_AnalysisRuns` passaram); a falha
  do `Should_RunInBackground_When_Generating` era o teste somando só Comprar + Promover + Manter: na suíte completa outros testes deixam
  estoque desequilibrado e saem recomendações "Transferir". Corrigido; testes da previsão 35/35, `dotnet format` limpo. Front 81/81,
  build ok, lint de `src` ok (o `npm run lint` acusa os exemplos da skill em `.agents/skills/shadcn/assets/showcase`, fora do app).
- **Pedido 1 (diálogos):** o comprar não exige o local de entrega do grupo quando todos os itens estão divididos por loja (mostra
  "cada loja recebe no próprio local"); loja dividida sem local de recebimento padrão vira erro na linha. Layout: falta o Daniel conferir.
- **Pedido 2 (divisão por loja):** coluna Sugestão mostra a parte de cada loja, detalhe ganha "Divisão por loja" e o comprar abre já
  dividido quando `storeSplit` tem 2+ lojas. Não feito (opcional): mandar a divisão no payload da IA.
- **Pedido 3:** "Promover selecionados" é a tela `/forecast/promote?ids=…` (`BulkPromoteForm`; aberta direto, recarrega pelos ids).
- **Pedido 4:** `/dashboard/low-stock` e `/dashboard/expiring-lots`; `storeId`/`storeName` nos itens; cada ação troca a loja do topo
  antes de abrir (comprar com a IA, novo pedido, promover, dar baixa). Em "todas as lojas" a linha mostra "Loja › Local".
- **Dev:** backend reiniciado. Para ver a divisão por loja e "Transferir", gerar nova análise (as recomendações antigas não têm divisão).
- **Continuam pendentes de decisão:** exceção ao ADR 0010 no seed; janela de 90 dias da participação por loja; janela de 30 dias do
  alerta de vencimento.

## 0.5 Atualização de 08/11/2026 (madrugada): muito feito, NADA commitado, pedidos em aberto

### Onde está o código (tudo no disco, sem commit)
| Repo | Branch | Conteúdo |
|--|--|--|
| `~/Projetos/nextflow/nextflow` (back) | `feat/seed-completo` (saiu da `homolog` `08e33bb`) | seed completo, filtro de status com lista, edição de promoção, filtro `eventId`, painel "ver mais", F3.9, F3.4b |
| `~/Projetos/nextflow/nextflow-front` | `feat/ajustes-vendas-compras` (saiu da `homolog` `13a0622`) | todas as telas abaixo |
| `~/Projetos/nextflow/nextflow-docs` | `main` | regras, contratos, cartões F3.9 e F3.4b, log |

Ao commitar, separar o back em partes (commit por caminho): seed; filtros (`FilterExpressionBuilder`, `eventId`); promoção (PUT);
painel; F3.9; F3.4b. Depois merge na `homolog` e push (o Daniel pediu "corrigidos esses, atualiza a doc e sobe tudo pra homolog").

### Migrations novas (nesta ordem)
`AddRecommendationPurchaseOrders` (F3.9, com SQL que preenche os pedidos já aplicados) → `AddStockTransfers` (F3.4b; **já aplicada
no banco de dev** pelo `dotnet watch`, não remover) → `AddRecommendationStores` (divisão por loja gravada pela análise, recém-criada,
ainda não testada).

### Feito nesta sessão (detalhe em `implementation-log.md`)
- Seed: vendedores, coleções, promoções e pedidos de compra em todos os status, lotes vencendo, retomada do histórico (transação por
  dia), depósito só com o que não vence, fotos, e transferência errada Shopping → Centro em 4 alimentos (gera "Transferir").
- Telas: search select, detalhe de venda (cores), histórico (nº abre detalhe), pedidos de compra (filtro de status múltiplo, Receber,
  layout em 2 colunas, busca de item igual à venda), venda rápida repaginada + leitor fora da busca, baixa de lote, mobile (cards,
  abas em grade, `meta.hideOnMobile`/`meta.label`), margem no produto, promoções (editar agendada, visualizar), coleções e
  calendário (visualizar), painel com "ver mais", previsão com promover/descartar selecionados.
- F3.9 (comprar dividido por loja) e F3.4b (Transferir completo) implementadas; regras RN-DF27/28/29 e RN-CE62 aprovadas.

### Estado dos testes
- Front: 80/80, build e lint ok (antes dos pedidos abaixo).
- Back: última suíte completa 1044/1045. Falhou `ForecastApiTests.Should_RunInBackground_When_Generating` (passa sozinho;
  investigar se é instabilidade ou efeito do seed novo). Depois disso entraram `AddRecommendationStores`, o cálculo por loja no motor
  (`ForecastEngine.WithStoreSplit`) e o teste `Should_SplitBuyAcrossStores_When_AnalysisRuns`: **nada disso foi rodado ainda**.
- Ajustei 2 testes do `ForecastEngineTests` para a ação Transferir (itens e motivo sem IA).

### Pedidos do Daniel em aberto (último recado, com prints)
1. **Layout quebrado nos diálogos** (Transferir estoque: botão vazando e nomes cortados; Gerar pedido de compra: barra de rolagem
   horizontal e "Escolha o local" vazio com "todas as lojas"). Já feito: `DialogContent` com `[&>*]:min-w-0` e largura
   `calc(100%-2rem)`; card do Transferir com "De/Para" quebrando linha. **Falta conferir** e, no comprar, não exigir local do grupo
   quando todos os itens estão divididos por loja.
2. **A análise deve recomendar a quantidade de cada loja**, não só o total. Feito no back (não testado): `ForecastRecommendationStore`
   (tabela `forecast_recommendation_stores`), `ForecastEngine.WithStoreSplit` divide todo "Comprar" pela falta de cada loja e acrescenta
   "Por loja: …" ao motivo (e ao motivo calculado), `ListItem.storeSplit`, e o `store-split` usa a divisão gravada. **Falta:** rodar os
   testes; no front, mostrar a divisão na coluna Sugestão e no detalhe, e abrir o dialog de comprar já dividido (ligar
   `enableSplit` automático quando `storeSplit` tem 2+ lojas). Opcional: mandar a divisão no payload da IA para ela explicar.
3. **"Promover selecionados" deve ser uma tela, não modal.** Proposta: rota `/forecast/promote?ids=…` reaproveitando o
   `BulkPromoteForm` de `bulk-promote-dialog.tsx`.
4. **"Ver mais" do painel deve ser tela, e as ações devem trocar a loja do topo** (com "todas as lojas" o comprar não sabe a loja).
   Proposta: rotas `/dashboard/low-stock` e `/dashboard/expiring-lots` (conteúdo dos dialogs de `dashboard-more-dialogs.tsx`), back
   devolvendo `storeId` em `LowStockItemDto` e `ExpiringLotItemDto` (a linha do repositório já tem `LocationId`), e cada ação chama
   `setStoreId(item.storeId)` (`useCurrentStore`) antes de abrir o comprar, o promover ou a aba Lotes.
5. Depois: atualizar os docs (contratos das rotas novas, board, este handoff) e **subir tudo para a `homolog`** (commit por partes,
   merge, push).

### Lembretes
- Classe nova no back exige `docker compose -f compose.development.yaml restart backend` (o hot reload não registra na DI).
- Dev: front `http://localhost:5174`, API `8081`, login `admin@nextflow.com` / `!Admin123`. Para ver "Transferir", gerar nova análise.
- Pendências de decisão do Daniel: exceção ao ADR 0010 no seed (transação por dia); janela de 90 dias da participação por loja;
  janela fixa de 30 dias do alerta de vencimento.

## 0.4 Atualização de 08/11/2026 (noite): tudo junto na homolog
- **Back e front:** bloco C, `feat/filtro-loja`, `feat/historico-vendas`, `feat/venda-rapida-ajustes` e (só front) `feat/forecast-acoes`
  juntados na `homolog` e já no `origin/homolog` (back `97f78b5`, front `13a0622`). Hashes de cada merge em `slices/board.md`,
  seção "Juntado na homolog".
- **Seed de fotos:** `DemoPhotosSeeder` (`c46b1c0`) baixa as fotos dos produtos demo do Unsplash (ids do catálogo v1) e sobe no Silo,
  só para produto demo sem imagem; sem rede, a foto fica de fora com aviso no log e o startup segue. Juntado na `homolog` do back
  (`08e33bb`), **sem push**. Suíte 1012/1012, `dotnet format` limpo, build `-warnaserror` ok.
- **Organização:** branches das frentes apagadas e worktrees removidos (`nextflow-loja`, `nextflow-hist`, `nextflow-venda`,
  `nextflow-front-*`, `nextflow-seedimg`). Daqui em diante, uma branch por frente no checkout principal, sem pasta por tarefa.
- **Seed completo (`feat/seed-completo`, back):** vendedores, coleções, promoções e pedidos de compra em todos os status, lotes
  vencendo em até 30 dias e retomada do histórico interrompido. O banco de dev de 08/11 tinha o histórico cortado em abr/2025
  (seed interrompido), então para testar: `docker compose -f compose.development.yaml down -v` e subir de novo.
- **Retomar por aqui:** (1) push do back quando o Daniel pedir; (2) QA do Daniel dos blocos A, B e C e das frentes; (3) backlog do
  Daniel (`slices/board.md`), cada item vira cartão antes do código.

## 1. Onde está o quê
| Repo | Remoto | Branch de trabalho | Último commit (07/11) |
|--|--|--|--|
| API .NET 10 | `git@github.com:Dan1elz/nextflow.git` | `homolog` | `89d3c3c` feat(cadastros) |
| Front React + shadcn | `git@github.com:Dan1elz/nextflow-front.git` | `homolog` | `c442a77` fix(front) abas do produto |
| Docs | `git@github.com:Dan1elz/nextflow-docs.git` | `main` | `aa4bf12` first commit + este handoff |

- O código da `homolog` dos dois repos já está todo no `origin/homolog`. Ficaram **sem push** só os commits de
  documentação deste handoff (07/11): `docs(setup)` no back e no front (`docs/local-setup.md`) e o commit `docs: handoff`
  na `nextflow-docs`. Para subir: `git push` em cada um.
- `main` dos dois repos é o app antigo (staging atual); `task-17` guarda o código antigo de referência.
- Branches locais extras no back (só nesta máquina, sem remoto): `dev/sem-f17` (2 cherry-picks de compose que já estão
  na `homolog` como `b331763` e `5587e34`; pode apagar) e `wip/stash-task-17` (stash antigo da task-17, só referência).
- Dev era no Windows (`C:\Projetos\Pessoal\nextflow`, cópia antiga, **não usar**); desde 07/11 é o WSL
  (`~/Projetos/nextflow`).
- VM (`ssh pessoal`): dev da API nova em `~/projects/nextflow-v2/` (compose `compose.vm-dev.yaml`, branch `homolog`);
  staging (app antigo) em `~/projects/nextflow/`. Em 07/11 outra IA deixou na VM um commit sem push (`7239f4e`, só
  `Seed__Demo__HistoryMonths` no `compose.vm-dev.yaml`; a `homolog` já tem o equivalente em `b331763`).

## 2. Estado por bloco e fatia
| Bloco | Fatias | Estado |
|--|--|--|
| 0 Fundação | F0.1–F0.6 | Feito |
| A Catálogo e estoque | F1.1–F1.6, F1.8, F1.11 | Aprovadas (F1.6 sem registro de review); QA do bloco A com o Daniel |
| B Venda e compra | F2.1 seletor, F2.3 promoções, F2.4 venda rápida, F2.7 pedido de compra, F2.8 recebimento, F2.9 seed 36 meses | **Prontas e commitadas, aguardando QA do Daniel** |
| B (fora de cartão) | histórico de vendas e `GET /api/orders`; cadastros de 07/11 | Aguardando QA |
| — | F1.7 Lotes com validade (FEFO) | **Pronta, aprovada na review, aguardando QA** |
| B | F2.5 pedido com orçamento | **Fora do escopo** (Daniel, 07/11). A tela `/orders` mostra um aviso no lugar |
| B | F2.10 push e troca do staging | A cargo do Daniel |
| C Previsão | F3.1–F3.5, F3.7, F3.6a–c, F3.4c (back); F3.8a–i (front) | **Feito em branches locais (08/11), aguardando QA do Daniel** (seção 0.3) |
| Opcional | F2.2, F2.6, F1.9, F1.10, F3.4b | Só depois do bloco C (a F3.6 foi feita em 08/11) |

QA final é sempre do Daniel, por bloco.

## 3. Decisões de produto e escopo
- **Escopo do TCC:** só o perfil Admin. Fora: financeiro, PDV completo, troca, fiado, NF-e. F2.5 (orçamento) fora.
- **Custo médio** por variação (ponderado na entrada; `product_variants.version` como token de concorrência, F2.8).
- **Estoque como livro-razão** (ADR 0007): saldo = soma dos movimentos; só o `IStockLedger` escreve; movimento imutável.
- **Estoque negativo bloqueado** por padrão, liberado por produto com a flag "permite negativo" (RN-CE32).
- **Mínimo por local** (variação × local), com padrão do produto e política ABC (F1.8).
- **Variação como unidade de estoque** (ADR 0008): produto sem grade tem uma variação padrão oculta.
- **Lojas e locais de estoque** (ADR 0009): cada loja com locais (ex.: "Loja", vendável, e "Depósito", recebimento).
- **Lotes/FEFO** (F1.7): saldo por variação × local × lote; saída sem lote escolhido sai do que vence primeiro
  (vencidos inclusive); produto com lote nunca fica com saldo sem lote (variação sem lote algum → 422); lote que fica
  negativo só some com ajuste manual nesse lote (limitação aceita pelo Daniel); `balanceAfter` do kardex = saldo do
  lote; ligar/desligar "controla lote" com saldo → 422 (RN-CE55).
- **Alerta de vencimento com janela fixa de 30 dias:** implementado, **pendente de confirmação do Daniel**.
- RN-CE15 (FEFO) foi implementada a partir de um rascunho: segue "a validar com o Daniel".
- **Banca:** dezembro de 2026 (data a confirmar). Se apertar, saem nesta ordem: F1.9, F1.10, F3.6, F3.4b
  (`implementation-plan.md`).

## 4. Pendências abertas
1. Re-review leve da F2.7 (correção c4f9fc9) e da F2.4 (9d4b21f + 24bbd75).
2. Seed F2.9: recebimento datado às 10h → 8h (no `Receive` e no `lastCosts` do `DemoHistorySeeder`).
3. Selo amarelo "vence em até 30 dias" (front e7cb149): QA visual; e confirmar a janela de 30 dias.
4. QA das correções de venda rápida e promoções, do histórico de vendas e dos cadastros de 07/11.
5. **Bug do motor de previsão:** item zerado (de temporada, fora de época) aparece como "Comprar alta". Previsto na
   F3.7, junto do motor portado (F3.2); aguardando decisão do Daniel.
6. F1.6 sem review registrada; QA do bloco A.
7. **Próxima etapa, bloco C** (`implementation-plan.md` e `slices/README.md`): F3.1 dados derivados
   (`product_sales_monthly`, `stock_daily_snapshots`, `product_seasonality`) → F3.2 motor portado (densa) + F3.7 bug da
   temporada → F3.3 análise em segundo plano → F3.4 ações Comprar/Promover/Manter/Descartar (densa) → F3.5 painel e
   notificações (inclui lote vencendo). Os cartões do bloco C ainda não existem: escrevê-los a partir do código real.

## 5. Setup do zero em outra máquina
Conferido contra `compose.development.yaml`, `.env.example`, `appsettings.Development.json`, `UsersSeeder` e os
compose do front em 07/11.

1. **WSL + Docker.** No PowerShell (admin): `wsl --install -d Ubuntu`. Instale o Docker Desktop e ligue
   *Settings → Resources → WSL integration* para a distro.
2. **Git e SSH** dentro do Ubuntu: `sudo apt install -y git`, crie a chave (`ssh-keygen -t ed25519`) e cadastre a
   pública no GitHub.
3. **Clonar** (dentro do Linux, não em `/mnt/c`):
   ```
   mkdir -p ~/Projetos/nextflow && cd ~/Projetos/nextflow
   git clone -b homolog git@github.com:Dan1elz/nextflow.git
   git clone -b homolog git@github.com:Dan1elz/nextflow-front.git
   git clone git@github.com:Dan1elz/nextflow-docs.git
   ```
4. **`.env`: não precisa.** Os dois compose de dev têm padrões para tudo. Se criar o do back a partir do
   `.env.example`, apague `STORAGE_PORT`, `STORAGE_CONSOLE_PORT` e `STORAGE_PUBLIC_URL` (trocam 9010/9011 por
   9000/9001). `SEED_ADMIN_PASSWORD` é ignorada no dev. Não reaproveite `.env` do v1 (outra senha de Postgres e outras
   portas). A chave da IA (`AI_API_KEY`) é opcional e nunca vai para o git.
5. **Subir a API** (Postgres, storage S3 e API em watch):
   ```
   cd ~/Projetos/nextflow/nextflow
   docker compose -f compose.development.yaml up -d --build
   docker compose -f compose.development.yaml logs -f backend
   ```
   API `http://localhost:8081` (Swagger `/swagger`), Postgres `localhost:5435`, storage `:9010` (painel `:9011`).
6. **Migrations e seed demo** rodam sozinhos no startup (`MigrateAsync` no `Program.cs`). O seed demo
   (`Seed:Demo:Enabled`, padrão ligado) cria a loja de doces e presentes com 36 meses de histórico
   (`Seed:Demo:HistoryMonths=36` no `appsettings.Development.json`): espere de 3 a 5 min no primeiro startup.
7. **Login:** `admin@nextflow.com`, senha de dev na constante `DevelopmentPassword` de
   `nextflow.Infrastructure/Seeders/UsersSeeder.cs`.
8. **Front com hot reload:**
   ```
   cd ~/Projetos/nextflow/nextflow-front
   docker compose -f compose.development.yaml up -d --build
   ```
   Abra `http://localhost:5174`. Opcional: build de produção no nginx pelo compose do back,
   `docker compose -f compose.development.yaml --profile front up -d --build` → `http://localhost:8082`
   (outro caminho do front: `FRONT_CONTEXT`).
9. **Ferramentas para desenvolver** (testes, migration nova, lint): .NET 10 SDK (ex.: em `~/.dotnet`) e Node via nvm.
   Migration nova: `dotnet ef migrations add <Nome> --project nextflow.Infrastructure --startup-project nextflow`.
   Banco do zero (migration ou seed novos): `docker compose -f compose.development.yaml down -v` e subir de novo.

Pegadinhas: em shell não interativo do WSL, `dotnet`/`node` só existem se exportar o `PATH`; pasta com barra
invertida no nome (sobra de build do Windows) quebra o MSBuild (`MSB3552`), ache com `find . -name '*\\*'`;
containers subidos do Windows precisam ser derrubados antes de subir pelo WSL.

## 6. Esteira de dev, economia de tokens e estilo de trabalho
Os arquivos `nextflow-dev-pipeline.md`, `nextflow-token-audit.md`, `nextflow-working-style.md` e
`nextflow-product-decisions.md` **não existem no disco** (procurei no WSL e no Windows): estão só na memória do projeto
no Claude. O que está versionado: `slices/README.md` (esteira e ordem dos blocos), `slices/rules-cheatsheet.md` e
`implementation-plan.md`. Resumo das regras:
- **Uma fatia (uma thread de código) por vez**, sem paralelo no mesmo checkout: a migration EF puxa o modelo de qualquer
  WIP no disco (`ApplyConfigurationsFromAssembly`) e o `AppDbContextModelSnapshot.cs` colide.
- **Correção pequena volta para a thread de dev** da fatia, não abre thread nova.
- **Review em thread separada só para fatias densas** (F1.5, F2.4, F2.8, F1.7, F3.2, F3.4…); as demais, review leve.
- **A thread de dev recebe só o cartão + `rules-cheatsheet.md`** (e trechos do contrato por `grep`), nunca os guias
  inteiros.
- **TDD:** cartão com critérios de aceite e testes escritos antes do código; os testes do cartão são obrigatórios e com
  esses nomes; sem RN nova (caso de borda vira 400/422 e uma linha em "Em aberto").
- Sem build/lint/teste a cada passo: uma vez antes de subir (`dotnet format --verify-no-changes`,
  `dotnet build -warnaserror`, testes, `npm run lint`, `npm run build`).
- Conferência visual das telas é do Daniel (a IA para em build e lint, sem Playwright).
- Commit por caminho (`git add <arquivos>`), mensagem em português, push só no fim do bloco.
