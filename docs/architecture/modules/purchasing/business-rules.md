# Módulo Compras — regras de negócio

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** código da API (PurchaseOrders), decisão R5 do review

| ID | Regra | Fonte | Data | Status |
|--|--|--|--|--|
| RN-CP01 | Pedido de compra precisa de ao menos um item | `CreatePurchaseOrderUseCase` | 2026-10-11 | comportamento atual |
| RN-CP02 | Ao receber: uma entrada de estoque por item, grava `ReceivedAt` e atualiza `CostPrice` do produto | `UpdatePurchaseOrderUseCase` | 2026-10-11 | comportamento atual |
| RN-CP03 | Pedido recebido não muda de status nem de itens (não cancela) | Código; decisão 0001 (R5) | 2026-10-27 | decidido (rascunho) |
| RN-CP04 | Não existe recebimento parcial: recebe-se o pedido inteiro | Decisão 0001 (R5) | 2026-10-27 | decidido (rascunho) |
| RN-CP05 | Itens de pedidos em Orçamento ou Pendente contam como "estoque a chegar" na previsão | `AI_FORECAST_SPEC.md` §5 | 2026-10-11 | comportamento atual |
| RN-CP06 | (substituído por RN-CP08 quanto ao início) Lead time real = média (`ReceivedAt − CreateAt`) dos últimos 5 recebidos do fornecedor; sem histórico, o cadastrado | `PROJECT.md` §5.1.1 | 2026-10-11 | comportamento atual |
| RN-CP07 | Fluxo mantido (Orçamento → Pendente → Recebido / Cancelado); acrescenta local de entrega e lote/validade no recebimento; compra sempre na unidade de venda | Entrevista compras, item 5 | 2026-10-28 | validado |
| RN-CP08 | Pedido de compra tem o passo "Enviar ao fornecedor" (Orçamento → Pendente, grava a data de envio); lead time real = recebimento − envio | Lacuna L-CP3 | 2026-10-28 | validado |

## Perguntas em aberto
- RN-CP05: orçamento de compra ainda não enviado ao fornecedor deveria contar como "a chegar"?
- RN-CP06: o lead time deveria contar da data de envio (Pendente), não da criação?
