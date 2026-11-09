# Módulo Inteligência de compras — regras de negócio

> **Status:** rascunho / a validar · **Atualizado:** 2026-11-08
> **Origem:** `nextflow/docs/AI_FORECAST_SPEC.md` §5 e §6.5 (11/10/2026)

| ID | Regra | Fonte | Data | Status |
|--|--|--|--|--|
| RN-DF01 | Só Admin gera análise; geração sob demanda, sem job agendado | spec §2 e §10 | 2026-10-11 | substituído por RN-DF18 |
| RN-DF02 | Base: vendas com pagamento confirmado, agregadas por mês no fuso de negócio, últimos 36 meses; cálculo usa até 24 meses completos | spec §2 e §5 | 2026-10-11 | comportamento atual |
| RN-DF03 | Índice sazonal do produto (≥ 12 meses) combinado com o da categoria por peso `min(1, meses/24)`, limitado a [0,05; 5] | spec §5.2–5.4 | 2026-10-11 | comportamento atual |
| RN-DF04 | Produto sazonal sem vendas recentes (≥ 12 meses e últimos 6 < 15% dos últimos 12) projeta pelo mesmo mês do ano anterior × tendência [0,8; 1,25] | spec §5 Regra 5b | 2026-10-11 | comportamento atual |
| RN-DF05 | Confiança: < 6 meses Baixa; 6–17 Média; ≥ 18 Alta | spec §5.7 | 2026-10-11 | comportamento atual |
| RN-DF06 | Necessidade de compra = demanda em (lead time + 30 dias) + estoque de segurança (máx. entre `MinStock` e 25% do próximo mês) − estoque − a chegar | spec §5.9 | 2026-10-11 | comportamento atual |
| RN-DF07 | Promover se: excesso (estoque > 1,5× demanda do horizonte e baixa temporada) ou validade em até 60 dias com sobra; nunca com promoção vigente | spec §5.10 | 2026-10-11 | comportamento atual |
| RN-DF08 | Desconto sugerido preserva 10% de margem sobre o custo, entre 5% e 25%; sem margem para 5%, não promove | spec §5.11 | 2026-10-11 | comportamento atual |
| RN-DF09 | Produto sem venda no período → Manter, confiança Baixa, não vai para a IA | spec §5.13 | 2026-10-11 | comportamento atual |
| RN-DF10 | A IA não altera a confiança; produto ausente na resposta usa o cálculo | spec §6.5 | 2026-10-11 | comportamento atual |
| RN-DF11 | "Comprar" da IA sem necessidade calculada vira "Manter" | spec §6.5 | 2026-10-11 | comportamento atual |
| RN-DF12 | Quantidade de compra da IA limitada a 0,5×–1,5× da calculada; desconto a [5%, máx.]; dias de promoção a [7, 45] | spec §6.5 | 2026-10-11 | comportamento atual |
| RN-DF13 | Falha ou ausência da IA → análise só com o cálculo e motivos em template (`CompletedWithoutAi`) | spec §6.5 | 2026-10-11 | comportamento atual |
| RN-DF14 | Nova análise expira as recomendações pendentes da anterior | spec §2 | 2026-10-11 | comportamento atual |
| RN-DF15 | Aplicar "Comprar" gera um pedido de compra em Orçamento por fornecedor; nada é enviado automaticamente | spec §1 e §7.1 | 2026-10-11 | comportamento atual |
| RN-DF16 | Nova ação **Transferir**: se um local está abaixo do mínimo e outro tem excesso (acima da cobertura alvo) da mesma variação, a IA recomenda transferir antes de recomendar comprar | Entrevista estoque, item 4 | 2026-10-28 | validado; detalhe aprovado em 08/11 (F3.4b): por variação, local A abaixo do mínimo e local B com excesso = disponível − cobertura alvo (política ABC) × demanda diária de B; quantidade = min(falta de A até o mínimo, excesso de B); a falta coberta não gera "Comprar" |
| RN-DF17 | Horizonte automático = maior prazo de entrega dos produtos + 3 meses, com teto de 6 meses (substitui o seletor fixo de 1 a 3) | Entrevista sazonalidade, item 1 | 2026-10-28 | validado |
| RN-DF18 | Análise roda sozinha uma vez por semana e também pelo botão manual; recomendação nova gera notificação no sistema | Item 2 | 2026-10-28 | validado |
| RN-DF19 | Cada projeção é comparada com o vendido do mês (erro absoluto e %), com precisão exibida por produto | Item 3 | 2026-10-28 | validado |
| RN-DF20 | O cálculo e a IA cobrem todos os produtos; a IA recebe lotes sequenciais de até N produtos (N inicial 40), o próximo só após a resposta do anterior; um lote com falha cai para o cálculo sem derrubar a análise; o resumo geral é feito numa chamada final com os resultados dos lotes | Item 4 | 2026-10-28 | validado |
| RN-DF21 | A recomendação é por produto e a quantidade é rateada nas variações pela proporção histórica de venda da grade | Item 5 (e RN-CE16) | 2026-10-28 | validado |
| RN-DF22 | Limites da IA mantidos (prioriza, explica, ajusta quantidade entre 0,5× e 1,5× do calculado, confiança sempre do cálculo); Transferir entra como ação nova | Item 6 | 2026-10-28 | validado |
| RN-DF23 | A análise roda em segundo plano (status "Em andamento" com progresso dos lotes); só uma por vez; ao terminar gera notificação | Lacuna L-DF1 | 2026-10-28 | validado |
| RN-DF24 | Previsão zerada na janela de compra (lead time + 30 dias) vira **"Sem ação"**: grava `Hold` com o motivo "Sem ação: nenhuma demanda prevista nos próximos N dias", nunca "Comprar" (o enum não muda; o rótulo "Sem ação" × "Manter" na tela é decisão do front) | Review F3.2/F3.7 (08/11) | 2026-11-08 | validado (Daniel, 08/11: sem aviso separado por ora) |
| RN-DF25 | A IA não cria ação sem gatilho do cálculo: "Promover" só vale quando o cálculo achou excesso em baixa temporada ou validade (RN-DF07); um "Manter" do cálculo não vira "Promover" pela IA (complementa RN-DF11 e ADR 0005) | Review F3.2 (08/11) | 2026-11-08 | validado (Daniel, 08/11) |
| RN-DF26 | Precisão (RN-DF19): produto "dentro da tolerância" quando o erro médio (MAPE) é **≤ 15%**; viés só quando a média do erro com sinal passa de **±5%**; mês com **mais de 50% dos dias sem estoque** fica fora da medição, assim como vendido zero com previsto acima de zero | F3.6a, L-DF3 | 2026-11-08 | validado (Daniel, 08/11: tolerância 20% → 15%) |
| RN-DF27 | Ao aplicar "Comprar", a quantidade pode ser dividida entre lojas. Sugestão por loja: falta = max(0, demanda do horizonte × participação da loja − saldo da loja − a caminho para a loja), participação = vendas da loja nos últimos 90 dias ÷ vendas da empresa; a quantidade sugerida é rateada pela falta (sem falta em nenhuma, pela participação), arredondada ao múltiplo do fornecedor, com o resto na loja de maior falta. O Admin ajusta antes de gerar; um pedido por fornecedor × loja | Pedido do Daniel, cartão F3.9 | 2026-11-08 | validado (Daniel, 08/11) |
| RN-DF28 | Recomendação aplicada pode ter vários pedidos de compra (um por fornecedor × loja); volta a Pendente só quando todos forem cancelados | Cartão F3.9 | 2026-11-08 | validado (Daniel, 08/11) |
| RN-DF29 | A IA só prioriza e explica "Transferir"; não cria transferência sem o gatilho do cálculo (como RN-DF25) | Cartão F3.4b | 2026-11-08 | validado (Daniel, 08/11) |
| RN-DF30 | Sugestão sob demanda no "ver mais" do painel, para qualquer linha (mesmo sem recomendação na última análise): **compra** de uma variação num local = volta ao mínimo e cobre prazo de entrega do fornecedor preferido + 30 dias da venda média da loja (90 dias), menos o que está a caminho, nunca menos que a falta até o mínimo, no pedido mínimo e no múltiplo; **promoção** de um lote = 5% se a venda normal até o vencimento escoa o lote, senão 5% + sobra × 20 p.p. em passos de 5%, até min(25%, máximo da margem), até a véspera do vencimento. A IA revisa dentro de RN-DF12 (compra 0,5×–1,5× do calculado; desconto 5% ao máximo da margem; dias 7 a 45, sem passar do vencimento) e explica; sem IA, fica o cálculo. "Novo pedido de compra" usa só o cálculo (sem gastar cota) | Pedido do Daniel (08/11, prints do painel) | 2026-11-08 | **a aprovar** (cartão F3.10) |

## Perguntas em aberto
- RN-DF08: 10% de margem mínima é regra do lojista ou um palpite técnico? Deveria ser configurável?
- RN-DF06: janela fixa de 30 dias após o lead time faz sentido para todo segmento?
