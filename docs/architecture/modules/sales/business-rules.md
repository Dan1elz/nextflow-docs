# Módulo Vendas — regras de negócio

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** código da API (Orders, Sales, Promotions), `AI_FORECAST_SPEC.md`, decisões do review

| ID | Regra | Fonte | Data | Status |
|--|--|--|--|--|
| RN-VD01 | Pedido precisa ter ao menos um item | `CreateOrderUseCase` | 2026-10-11 | comportamento atual |
| RN-VD02 | Preço do item = preço efetivo do produto no dia (com promoção vigente), calculado só no backend | `IProductPricingService`; spec §4 | 2026-10-11 | comportamento atual; orçamento ajustado por RN-VD19 |
| RN-VD03 | Desconto é em R$ por item; o total do pedido é líquido | Decisão 0001 (R1) | 2026-10-27 | decidido (rascunho) |
| RN-VD04 | Só pedidos em Orçamento ou Aguardando pagamento podem ser editados | `UpdateOrderUseCase` | 2026-10-11 | comportamento atual |
| RN-VD05 | Checkout só para Orçamento ou Aguardando pagamento; soma dos pagamentos = total do pedido | `CreateSaleUseCase` | 2026-10-11 | comportamento atual |
| RN-VD06 | Confirmar pagamento exige estoque suficiente e gera movimentação de venda por item | `UpdateStatusByOrderIdUseCase` | 2026-10-11 | comportamento atual |
| RN-VD07 | Cancelar pedido que não é orçamento, ou reembolsar, devolve o estoque (movimentação de devolução) | `UpdateStatusByOrderIdUseCase` | 2026-10-11 | comportamento atual |
| RN-VD08 | Reembolso: um único caminho, só Admin, até 7 dias | Decisão 0002 (R3) | 2026-10-27 | decidido (rascunho) |
| RN-VD09 | Excluir venda até 48 h após o pedido gera reembolso; estorno do pedido só até 7 dias após a última atualização | `DeleteSaleUseCase`, `diagramas.md` | 2026-10-11 | comportamento atual, **substituído por RN-VD08** |
| RN-VD10 | Promoção: desconto de 1% a 90%; início ≥ hoje; término ≥ início; máx. 90 dias contando início e fim | `CreatePromotionUseCase`; spec §7.2 | 2026-10-11 | comportamento atual |
| RN-VD11 | Um produto não pode ter duas promoções ativas sobrepostas; produto precisa estar ativo | `CreatePromotionUseCase` | 2026-10-11 | comportamento atual |
| RN-VD12 | Promoção vigente = ativa e hoje entre início e término (inclusivo); cancelar = inativar | spec §7.2 | 2026-10-11 | comportamento atual |
| RN-VD13 | Promoção que deixa o preço abaixo do custo exibe aviso e exige confirmação | Decisão 0003 (R4) | 2026-10-27 | decidido (rascunho) |
| RN-VD14 | Orçamento tem validade (7 dias, provisório) e reserva estoque enquanto válido | `../catalog-inventory/decisions/0001` (R7) | 2026-10-27 | decidido (rascunho) |

| RN-VD15 | Venda rápida de balcão no "caminho feliz": busca/bipa o produto, quantidade, forma de pagamento, conclui; cliente opcional. Sem caixa (abertura/sangria/fechamento), sem TEF, sem cupom fiscal, sem modo offline | Entrevista vendas, item 1 | 2026-10-28 | validado |
| RN-VD16 | Dois estados de negócio: orçamento (com validade, reserva estoque) e venda (paga). "Aguardando pagamento" deixa de existir como etapa separada | Item 2 | 2026-10-28 | validado |
| RN-VD17 | Troca fica fora do escopo por prazo; resolve-se com reembolso + nova venda | Item 3 (a critério do Claude) | 2026-10-28 | validado |
| RN-VD18 | Sem venda a prazo nem fiado; pagamento sempre à vista nas formas existentes | Item 4 | 2026-10-28 | validado |
| RN-VD19 | Orçamento congela o preço (e a promoção) do dia em que foi feito enquanto estiver válido; venda direta usa o preço efetivo do dia | Contrato, lacuna L-VD4 | 2026-10-28 | validado |
| RN-VD20 | Formas de pagamento: dinheiro, crédito, débito, transferência e Pix (boleto removido) | Lacuna L-VD6 | 2026-10-28 | validado |

## Perguntas em aberto
- RN-VD08: os 7 dias contam da data do pagamento? (o código atual conta da última atualização)
- Reembolso parcial (um item) existe?
