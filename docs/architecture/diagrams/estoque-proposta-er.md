# Estoque — modelo proposto (ER)

> **Status:** proposta para a entrevista de 28/10/2026, a validar · Itens 1 a 7 da rodada de estoque

```mermaid
erDiagram
  PRODUTO ||--|{ VARIACAO : "tem (P azul, G preta)"
  PRODUTO }o--o{ CATEGORIA : classifica
  PRODUTO ||--o{ UNIDADE_COMPRA : "converte (caixa = 12 un)"
  VARIACAO ||--o{ SALDO : "saldo por local"
  LOCAL ||--o{ SALDO : guarda
  VARIACAO ||--o{ LOTE : "lote opcional"
  LOTE ||--o{ SALDO : "saldo do lote"
  VARIACAO ||--o{ MOVIMENTACAO : registra
  LOCAL ||--o{ MOVIMENTACAO : "onde"
  LOTE |o--o{ MOVIMENTACAO : "de qual lote"
  INVENTARIO ||--|{ ITEM_CONTAGEM : conta
  ITEM_CONTAGEM ||--o| MOVIMENTACAO : "gera ajuste"
  USUARIO ||--o{ MOVIMENTACAO : "quem fez"

  PRODUTO {
    string nome
    bool controlaLote
    bool permiteNegativo
    string unidadeVenda
  }
  VARIACAO {
    string sku
    string codigoBarras
    string atributos
    decimal custoMedio
    decimal ultimoCusto
    decimal estoqueMinimo
  }
  LOCAL {
    string nome
    bool padrao
  }
  SALDO {
    decimal fisico
    decimal reservado
    decimal disponivel
  }
  LOTE {
    string codigo
    date validade
  }
  UNIDADE_COMPRA {
    string unidade
    decimal fator
  }
  MOVIMENTACAO {
    enum tipo
    enum motivo
    decimal quantidade
    decimal custoUnitario
    datetime data
  }
  INVENTARIO {
    enum escopo
    enum status
    datetime data
  }
  ITEM_CONTAGEM {
    decimal esperado
    decimal contado
  }
```

Tipos de movimentação: entrada por compra, saída por venda, devolução de cliente, devolução ao fornecedor,
transferência (sai de um local, entra no outro), ajuste de inventário e perda (motivo: quebra, vencimento, furto, uso interno).
`disponivel = fisico − reservado`; a reserva é calculada a partir dos orçamentos válidos.
