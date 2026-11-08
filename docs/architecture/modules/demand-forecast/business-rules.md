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
| RN-DF16 | Nova ação **Transferir**: se um local está abaixo do mínimo e outro tem excesso (acima da cobertura alvo) da mesma variação, a IA recomenda transferir antes de recomendar comprar | Entrevista estoque, item 4 | 2026-10-28 | validado (desenho a detalhar) |
| RN-DF17 | Horizonte automático = maior prazo de entrega dos produtos + 3 meses, com teto de 6 meses (substitui o seletor fixo de 1 a 3) | Entrevista sazonalidade, item 1 | 2026-10-28 | validado |
| RN-DF18 | Análise roda sozinha uma vez por semana e também pelo botão manual; recomendação nova gera notificação no sistema | Item 2 | 2026-10-28 | validado |
| RN-DF19 | Cada projeção é comparada com o vendido do mês (erro absoluto e %), com precisão exibida por produto | Item 3 | 2026-10-28 | validado |
| RN-DF20 | O cálculo e a IA cobrem todos os produtos; a IA recebe lotes sequenciais de até N produtos (N inicial 40), o próximo só após a resposta do anterior; um lote com falha cai para o cálculo sem derrubar a análise; o resumo geral é feito numa chamada final com os resultados dos lotes | Item 4 | 2026-10-28 | validado |
| RN-DF21 | A recomendação é por produto e a quantidade é rateada nas variações pela proporção histórica de venda da grade | Item 5 (e RN-CE16) | 2026-10-28 | validado |
| RN-DF22 | Limites da IA mantidos (prioriza, explica, ajusta quantidade entre 0,5× e 1,5× do calculado, confiança sempre do cálculo); Transferir entra como ação nova | Item 6 | 2026-10-28 | validado |
| RN-DF23 | A análise roda em segundo plano (status "Em andamento" com progresso dos lotes); só uma por vez; ao terminar gera notificação | Lacuna L-DF1 | 2026-10-28 | validado |
| RN-DF24 | Previsão zerada na janela de compra (lead time + 30 dias) vira **"Sem ação"**: grava `Hold` com o motivo "Sem ação: nenhuma demanda prevista nos próximos N dias", nunca "Comprar" (o enum não muda; o rótulo "Sem ação" × "Manter" na tela é decisão do front) | Review F3.2/F3.7 (08/11) | 2026-11-08 | proposta (a confirmar com o Daniel) |
| RN-DF25 | A IA não cria ação sem gatilho do cálculo: "Promover" só vale quando o cálculo achou excesso em baixa temporada ou validade (RN-DF07); um "Manter" do cálculo não vira "Promover" pela IA (complementa RN-DF11 e ADR 0005) | Review F3.2 (08/11) | 2026-11-08 | comportamento atual (a confirmar) |

## Perguntas em aberto
- RN-DF08: 10% de margem mínima é regra do lojista ou um palpite técnico? Deveria ser configurável?
- RN-DF06: janela fixa de 30 dias após o lead time faz sentido para todo segmento?
- RN-DF19 / L-DF3 (proposta da F3.6a, 08/11): mês com mais da metade dos dias sem estoque fica fora da medição de precisão;
  vendido zero com previsto acima de zero também fica fora. Tolerância ±20% e viés por ±5% são palpites técnicos.
