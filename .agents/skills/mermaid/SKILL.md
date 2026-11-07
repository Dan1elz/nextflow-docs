---
name: mermaid
description: Cria diagramas Mermaid (sequência, estados, ER, fluxo) para a documentação do Nextflow; use sempre que um processo ou modelo ficar mais claro em diagrama.
---

# Diagramas Mermaid

## Escolha do tipo
| Para mostrar | Tipo |
|--|--|
| Ciclo de vida (pedido, compra, recomendação) | `stateDiagram-v2` |
| Troca de mensagens entre front, API, banco e IA | `sequenceDiagram` |
| Modelo de dados | `erDiagram` |
| Processo de negócio ou dependências | `flowchart` |

## Regras
- Fonte da verdade é o código e as regras documentadas: cite os IDs `RN-*` nas notas do diagrama.
- Rótulos em português; nomes técnicos (entidades, rotas) como no código.
- Um diagrama por ideia; mais de ~15 nós, divida.
- Evite caracteres que quebram o Mermaid em rótulos (parênteses e dois-pontos: use aspas).
- Pergunte ao Daniel só o que o código não responde (ex.: regra futura); marque o diagrama como rascunho até validar.
