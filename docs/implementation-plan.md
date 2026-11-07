# Plano de implementação — Nextflow até a banca

> **Status:** rascunho / a validar · **Data:** 2026-10-29 · **Origem:** regras RN-* fechadas em 28/10, contratos de tela
> (`architecture/contracts/`), ADR 0010 (padrão atrena) e `nextflow/docs/DOMAIN_LEVELS.md`.
> **Quem executa:** Daniel + IA (os colegas do TCC não programam). **Prazo:** banca em dezembro/2026, data a confirmar.

## Como ler este plano
- O plano tem **fases** (0 a 3) e cada fase tem **fatias**. Uma fatia é vertical e pequena: o modelo, a configuração EF,
  o repositório, os DTOs e validators, os use cases, o controller, os testes, a tela no front e a atualização do `contract.md`.
  Esses passos seguem a ordem de `DOMAIN_LEVELS.md`, "Ordem de implementação recomendada".
- A IA executa **uma fatia por vez**, sem padrão novo e sem regra inventada (`dotnet-development-guidelines.md`, seção de IA).
  Se faltar uma regra, a fatia para e a pergunta vai para o Daniel.
- **Pronto** quer dizer as quatro coisas abaixo:
  - build e testes verdes;
  - as regras citadas cobertas por teste unitário;
  - a tela funcionando contra a API real;
  - o contrato atualizado se o DTO divergiu.
- Os commits seguem a branch nova (o código antigo fica em `task-17` como referência) e cada fatia vira um PR ou commit
  revisável pelo Daniel.
- O seed demo (loja de doces e presentes, 36 meses, flag `Seed:Demo:Enabled`) cresce **junto** com as fases. Ele não fica
  para o fim.

## Calendário proposto

| Semana | Período | Fase | Marco |
|--|--|--|--|
| 1 | 02/11 – 08/11 | 0. Fundação | API nova sobe com login e cadastros base no padrão novo |
| 2–3 | 09/11 – 22/11 | 1. Catálogo e estoque | Produto com grade, lojas, locais e saldo pelo livro-razão |
| 4–5 | 23/11 – 06/12 | 2. Vendas e compras | **Versão demonstrável**: o staging troca para a versão nova |
| 6 | 07/12 – 13/12 | 3. Sazonalidade e previsão | Análise no DER novo, seed de 36 meses e notificações |
| 7 | 14/12 – 20/12 | Folga | Correções, ensaio da banca e ajuste do texto do TCC |

**Se a banca for antes de 10/12**, os itens marcados ✂ saem para depois dela, nesta ordem: transferência (F1.9),
inventário (F1.10), precisão da previsão (F3.6), ação Transferir da IA (F3.4b). Se mesmo assim não der, apresentamos a
versão anterior (`task-17`), como já combinado.

---

## Fase 0 — Fundação (semana 1)

| Fatia | Back | Front | Regras / contrato | Pronto quando |
|--|--|--|--|--|
| F0.1 Esqueleto | Solução .NET 10 (`Nextflow.Domain/Application/Infrastructure/Api`) com o núcleo do atrena: `ResultDto` com `FieldErrors`, `PaginationDto`, `IResultFactory`, bases de use case, `IUnitOfWork`, `ApiController`, `GlobalResultMiddleware`, Scrutor, Serilog e projeto xUnit | — | ADR 0010 | `dotnet test` verde e um endpoint de saúde respondendo |
| F0.2 Banco limpo | Migration inicial vazia, Docker do Postgres, appsettings por ambiente, dev recriado | — | ADR 0010 | `docker compose up` e migration aplicam do zero |
| F0.3 Front base | — | shadcn conforme a skill (`cssVariables`, tokens), `api.service` com envelope novo (`PaginationDto`, `ResultDto`, `fieldErrors`, `confirm` → `confirmWarnings`), `types/enums.ts` com enums em string | `contracts/README.md` | Um formulário de exemplo mostra o erro por campo vindo da API |
| F0.4 Acesso | `users`, `/api/auth` (login, me), token de 8 h, senha forte, último acesso, bloqueio de inativar a si mesmo e o último Admin | T-AC1 login, T-AC2/T-AC3 usuários, T-AC4 meu perfil | `access/contract.md`, L-AC1..5 | Login e CRUD de usuário de ponta a ponta |
| F0.5 Localidade e cadastros | `countries`, `states`, `cities`, `addresses`, `contacts` (polimórfico com `CHECK`), `suppliers`, `clients` (CPF opcional e único) | T-CD1..T-CD4 | `purchasing/contract.md`, L-CP6, L-CP7 | Fornecedor e cliente com endereço e contato, filtro de aniversariantes |
| F0.6 Lojas e locais | `stores` ⇄ `stock_locations` (padrões de venda e recebimento no mesmo commit), `user_stores` | T7 lojas e locais | ADR 0009, `DOMAIN_LEVELS.md` par 1 | Criar loja já cria o local "Loja" como padrão |

## Fase 1 — Catálogo e estoque (semanas 2 e 3)

| Fatia | Back | Front | Regras / contrato | Pronto quando |
|--|--|--|--|--|
| F1.1 Classificação | `categories` (2 níveis validados no use case), `collections` | T4, T5 | RN-CE23 | Categoria filha não aceita neta |
| F1.2 Calendário | `calendar_events` com o calendário comercial portado | T6 | RN-CE (eventos), `der-4` | Eventos padrão (Páscoa, Dia das Mães, Natal…) vêm no seed |
| F1.3 Produto e grade | `products` com `product_type` (Standard/Apparel/Perishable/Bulk), `product_attributes` e valores (`tempKey`), `product_variants` (variação padrão oculta), `product_variant_values`, `category_products`, imagens no S3 portado | T1 listagem, T2 formulário que muda os campos pelo tipo, T3 visualizar | ADR 0008, RN-CE16..29, L1 | Produto sem grade tem uma variação oculta; produto Apparel gera P/M/G |
| F1.4 Preço e fornecedor | `price_history` (grava em toda troca de preço), `product_suppliers`, `product_packagings` (múltiplo de compra), `product_events` (lead_days) | Abas do T2/T3 | RN-CE30, RN-CE (preço) | Mudar o preço grava o histórico com usuário e data |
| F1.5 Livro-razão | `IStockLedger` como único escritor; `stock_movements` imutável, `stock_balances` com `version`, custo médio por variação e bloqueio de negativo por flag | — | ADR 0007, RN-CE31, RN-CE32, RNF002 | Teste prova que saldo = soma das movimentações e que a concorrência devolve 409 |
| F1.6 Ajuste e abertura | Use cases de ajuste, perda e saldo de abertura (com custo, que entra no custo médio) | T9 drawer | L4, L5 | Abertura com custo muda o custo médio |
| F1.7 Lotes | `lots` (validade), saída FEFO dentro do ledger, alerta de lote vencendo | T12 | RN-CE09..13 | A venda tira primeiro do lote que vence antes |
| F1.8 Kardex e mínimos | Consulta de movimentações; `stock_location_minimums`; `stock_policies` (ABC) | T8, T13 | RN-CE33 | Kardex filtra por loja, local e variação |
| F1.9 ✂ Transferência | `stock_transfers` e itens, com status e número sequencial | T10 | ADR 0009, L-CP8 | Envio e recebimento movem os dois locais no ledger |
| F1.10 ✂ Inventário | `inventory_counts` e itens, contagem cega opcional, ajuste gerado no fechamento | T11 | L2, L3 | Diferença vira movimento de ajuste ligado ao item |
| F1.11 Seed do catálogo | Seed demo: lojas, locais, catálogo de doces e presentes com grade e lotes, saldo de abertura | — | — | `Seed:Demo:Enabled` recria o catálogo do zero |

## Fase 2 — Vendas e compras (semanas 4 e 5)

| Fatia | Back | Front | Regras / contrato | Pronto quando |
|--|--|--|--|--|
| F2.1 Seletor de venda | Endpoint de opções com preço efetivo e disponível por local | T-VD1 e aviso de falta T-VD1a | RN-VD (preço efetivo) | O seletor mostra o disponível do local de venda |
| F2.2 Falta de estoque | `lost_demand_records` | T14 dialog "procurou e não tinha" | RN-CE (demanda perdida) | O registro aparece no kardex e no histórico mensal |
| F2.3 Promoções | `promotions` (produto ou variação, sem conflito no período) com aviso abaixo do custo via `confirm` | T-VD7 | RN-VD13, L-VD5, L-VD10 | Promoção abaixo do custo pede confirmação |
| F2.4 Balcão | `orders` canal balcão, `order_items` (custo e lote congelados na baixa), `payments` (dinheiro, crédito, débito, transferência, Pix), tudo em um commit | T-VD2 venda rápida | RN-VD15..18, RN-VD20, ADR sales/0004 | Venda paga baixa o estoque no mesmo commit |
| F2.5 Orçamento | Orçamento com validade (7 dias, de 1 a 30), preço congelado, Expirado e Renovar, cancelar só o orçamento | T-VD3, T-VD4, T-VD5, T-VD6 checkout | RN-VD19, L-VD1..3, L-VD7 | Orçamento vencido não pode ser pago sem renovar |
| F2.6 Reembolso | Reembolso total em até 7 dias desde `paidAt`, devolvendo o estoque | Ação no T-VD5 | L-VD8, L-VD9 | O estoque volta pelo ledger |
| F2.7 Pedido de compra | `purchase_orders` e `purchase_items` por variação, com o múltiplo do fornecedor (avisa e confirma), "Enviar ao fornecedor" (`sentAt`) | T-CP1, T-CP2, T-CP3 | RN-CP07, RN-CP08, L-CP2 | O pedido enviado guarda o `sentAt` |
| F2.8 Recebimento | Recebimento no local de recebimento, com custo médio, lead time real = `receivedAt − sentAt`, divergência que abre ajuste e retroativo de até 7 dias | T-CP4, T-CP5 cancelar | RN-CP06, L-CP1, L-CP4 | Receber atualiza o custo médio e o lead time do fornecedor. Controle de concorrência no custo médio da variação (token de versão na variação; review da F1.5, 02/11) |
| F2.9 Seed de 36 meses | O seed gera vendas e compras de 36 meses pelos mesmos use cases ou pelo ledger, com sazonalidade de doces e presentes | — | RNF002 | Os saldos do seed batem com a soma das movimentações |
| F2.10 **Troca do staging** | Deploy da versão nova no staging | — | ADR 0010 | Demo de venda e compra de ponta a ponta no staging |

## Fase 3 — Sazonalidade e previsão (semana 6)

| Fatia | Back | Front | Regras / contrato | Pronto quando |
|--|--|--|--|--|
| F3.1 Dados derivados | Jobs de `product_sales_monthly` (com vendido em promoção, dias sem estoque e demanda perdida), `stock_daily_snapshots` e `product_seasonality` | — | `der-4`, L-DF3 | O recálculo bate com o seed |
| F3.2 Motor portado | `Forecast/` e `Services/Ai` portados para variação: horizonte automático de até 6 meses, rateio pela grade, lotes sequenciais de 40 para a IA (`forecast_ai_batches`) | — | RN-DF17..22, ADR 0005, L-DF2, L-DF5 | Testes de ida e volta do motor antigo continuam verdes |
| F3.3 Análise em segundo plano | `forecast_runs` com status Running e progresso, uma análise por vez, agendamento semanal e execução manual | T-DF2, T-DF9, T-DF11 | RN-DF23, L-DF1, L-DF7 | A tela mostra o progresso e notifica no fim |
| F3.4 Ações | Comprar (gera pedido de compra), Promover (gera promoção), Manter, Descartar; F3.4b ✂ Transferir | T-DF3, T-DF4, T-DF6, T-DF8; T-DF7 | RN-DF16, L-CP5, L-DF6 | Cancelar a compra gerada devolve a recomendação a Pendente |
| F3.5 Painel e notificações | `notifications` (resumo diário de estoque baixo e lote vencendo, aviso de análise concluída) | T-DF1 painel, T-DF12 sino, T-DF5 aba do produto | L-DF4, L-DF8 | O sino mostra a notificação da análise |
| F3.6 ✂ Precisão | `forecast_accuracy` (previsto × vendido) | T-DF10 | RN-DF (acurácia) | O gráfico mostra o erro por mês |
| F3.7 Bug da temporada | Corrigir o produto de temporada zerado fora da época, hoje marcado como "Comprar alta" (DP-015/016/044/045) | — | Pendente na thread do Silo | O seed não gera "Comprar alta" para item fora de época |

---

## Decisões em aberto que afetam o plano
| Decisão | Recomendação | Afeta |
|--|--|--|
| Data exata da banca | — | Cortes ✂ e semana de folga |
| Lado da FK entre a recomendação e o documento gerado | Na recomendação (`applied_purchase_order_id?` etc.) | F3.4 e a migration de N4 |
| Correção do motor (item de temporada zerado) | Corrigir em F3.7, já no motor portado | F3.2 e F3.7 |
| Código de cada fatia vai como PR ou commit direto na branch nova | PR por fatia, para o Daniel revisar | Ritmo das fases |
