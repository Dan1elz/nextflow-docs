# 0001 — Previsão da empresa inteira, com o estoque da loja ao lado

> **Status:** aceita em 08/11/2026 no pedido do filtro por loja (confirmar no QA do Daniel) · **Implementação:** em andamento na branch `feat/filtro-loja` (back e front, sem push)

## Contexto
O front tem uma **loja selecionada** no topo, e em 08/11 o Daniel pediu que ela filtre o painel, as listas e o novo pedido de compra.
A previsão (bloco C) calcula por produto somando todos os locais vendáveis da empresa (F3.2): histórico de vendas, saldo, "a caminho"
e mínimos são da empresa. Fazer uma previsão por loja exigiria histórico, sazonalidade e recomendações por loja, mais chamadas à IA e
um rateio de compra entre lojas.

## Decisão
- A análise continua **uma só, da empresa inteira**. Não há previsão por loja.
- Com uma loja no topo, as leituras da previsão aceitam `storeId` e devolvem também o **saldo da loja** e o **"a caminho" da loja**
  (`storeCurrentStock`, `storeIncomingStock`), mostrados ao lado do total da empresa, com aviso de que a sugestão vale para todas as lojas.
- Sem loja ("Todas as lojas"), os campos vêm nulos e a tela fica como antes.

## Consequências
- O motor, a IA e as tabelas da previsão não mudam; só a leitura soma o saldo por loja (`IStockBalanceRepository`) e o "a caminho" pelos
  locais de entrega da loja (`IPurchaseItemRepository`).
- **Revisitada em 08/11/2026:** o Daniel quer a previsão por loja (sazonalidade e necessidade de cada loja), mas fica para depois
  do TCC; o desenho está em `../../../../ideas/pos-tcc-previsao-por-loja.md`. Para a banca vale esta decisão, com a compra dividida
  pela falta de cada loja (RN-DF27).
- Transferir entre lojas (F3.4b, opcional) segue fora; quando entrar, é ela que aproveita a diferença entre lojas.
