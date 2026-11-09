# Diagramas de sequência

> **Status:** rascunho para o TCC, feito em 09/11/2026 a partir dos casos de uso, controllers e serviços reais
> (`CreateQuickSaleUseCase`, `ReceivePurchaseOrderUseCase`, `LoginUseCase`, `ForecastRunProcessor`, `ForecastEngine`,
> `ApplyPurchaseRecommendationsUseCase`, `GetPurchaseSuggestionUseCase`); aguarda revisão do Daniel. Feito em **Mermaid**
> (escolha do Daniel depois de comparar com PlantUML: mesma identidade das figuras anteriores).

Uma figura por fluxo principal, no nível do negócio: participantes em português e passos que o leitor entende, sem
nomes de métodos. Cores por camada: cinza = front-end, azul = back-end, ciano = serviço externo (IA).

## Figuras
| Figura sugerida | Arquivo | Substitui |
|--|--|--|
| Sequência — Autenticação e painel | [seq-1-autenticacao-painel.png](seq-1-autenticacao-painel.png) | Figura 11 |
| Sequência — Venda rápida no balcão | [seq-2-venda-rapida.png](seq-2-venda-rapida.png) | Figura 14 |
| Sequência — Pedido de compra: criar, enviar e receber | [seq-3-compra.png](seq-3-compra.png) | Figura 13 |
| Sequência — Ajuste e transferência de estoque | [seq-4-estoque.png](seq-4-estoque.png) | Figura 13 (parte de estoque) |
| Sequência — Análise de previsão de demanda | [seq-5-analise-previsao.png](seq-5-analise-previsao.png) | nova |
| Sequência — Aplicar recomendação Comprar | [seq-6-aplicar-comprar.png](seq-6-aplicar-comprar.png) | nova |
| Sequência — Sugestão da IA na hora (painel) | [seq-7-sugestao-ia.png](seq-7-sugestao-ia.png) | nova |

A antiga Figura 12 (gestão de cadastros) saiu: era só "valida e grava", padrão que já aparece nas outras.
Legenda no Word: "Figura N – Diagrama de sequência (Fluxo). Fonte: Elaborado pelo autor (2026)."
As figuras 3 e 7 são mais largas: melhor em página deitada.

## Como ler
- **Participantes** no topo, agrupados por camada; o **Livro-razão de estoque** aparece separado da API porque é o
  único caminho que altera saldo (RN-CE14) e o **Motor da previsão** porque roda em segundo plano.
- **Setas cheias** = pedido; **tracejadas** = resposta. Os **números** dão a ordem para o texto citar ("no passo 16...").
- **Faixa amarela** = fase do fluxo. **alt** = caminhos alternativos (um ou outro); **opt** = só acontece se a condição
  valer; **loop** = repete.
- As regras de negócio aparecem entre parênteses no próprio passo (RN-VD05, RN-DF12...).

## Roteiro para a banca
1. **Venda (2):** o preço vem da API, a baixa passa pelo livro-razão e tudo grava numa única transação (ou nada grava).
2. **Compra (3):** o ciclo Orçamento → Pendente → Recebido; o recebimento é que põe a mercadoria no estoque e atualiza o
   custo médio.
3. **Previsão (5):** o servidor calcula, a IA revisa em lotes dentro de limites, sem IA o sistema segue com o cálculo.
4. **Aplicar Comprar (6):** a recomendação vira pedido em orçamento por fornecedor e por loja; nada é enviado sozinho.

## Como estes diagramas foram montados (método reaproveitável)
1. **Escolher os fluxos que contam a história do sistema**, não um por tela: entrar e ver o painel, vender, comprar,
   mexer no estoque, analisar e aplicar. Cadastro simples (valida e grava) não precisa de diagrama próprio.
2. **Ler o caso de uso de verdade antes de desenhar.** Cada `return Failure(...)` vira um ramo `alt`/`opt`; cada
   chamada a outro serviço (livro-razão, IA, fila) vira um participante; cada `Commit` vira "confirma numa única transação".
   Foi assim que entraram a confirmação de preço da venda, a ausência de recebimento parcial e o "uma análise por vez".
3. **Nível do leitor:** participantes em português e mensagens com verbo do negócio ("baixar o estoque de cada item"),
   não `ledger.Post(document, lines)`. Mostrar só os participantes que ajudam a entender (front-end, API, serviços com
   regra própria, banco, serviço externo).
4. **Fases com faixa amarela** (`rect` + `Note over`) para quebrar fluxos longos; **numeração automática** para o texto.
5. **Regras no próprio passo**, entre parênteses, em vez de notas soltas.
6. **Revisar olhando a imagem**: mensagens longas alargam a figura; encurtar quando passar de uma página.

### Truques de Mermaid específicos de sequência
| Necessidade | Como |
|--|--|
| Agrupar participantes por camada com cor | `box rgb(227,242,253) Back-end` ... `end` |
| Fase do fluxo com faixa | `rect rgb(245,245,245)` + `Note over A,DB: Fase` ... `end` |
| Números nos passos | `autonumber` e `showSequenceNumbers: true` |
| Não repetir os participantes no rodapé | `mirrorActors: false` |
| Fonte legível no PNG | `themeVariables: fontSize: 18px` e `-s 2 -w 1600` |

## Como gerar as imagens
```bash
for f in seq-*.mmd; do
  docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/data" minlag/mermaid-cli:11.9.0 \
    -i "/data/$f" -o "/data/${f%.mmd}.png" -b white -s 2 -w 1600
done
```
