# Handoff — Nextflow (estado em 07/11/2026)

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
| C Previsão | F3.1, F3.2 + F3.7, F3.3, F3.4, F3.5 | A fazer (próxima etapa) |
| Opcional | F2.2, F2.6, F1.9, F1.10, F3.4b, F3.6 | Só depois do bloco C |

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
