# Diagramas de classes de implementação (referência técnica)

> **Para o TCC, use o modelo de domínio da pasta de cima** (`../README.md`). Esta versão é fiel ao código (nomes em
> inglês, tipos C#, todas as 48 classes) e serve de referência técnica ou apêndice. A figura de camadas ficou em `../`.

> **Status:** rascunho para o TCC, gerado em 09/11/2026 das **entidades C# do domínio** (`nextflow.Domain/Models` e
> `Enums`); aguarda revisão do Daniel. Feito em **PlantUML** (escolha do Daniel depois de comparar com Mermaid: UML
> completa, multiplicidades legíveis e layout mais compacto).

13 figuras: a das **camadas**, **11 por módulo** (48 classes) e uma com as **27 enumerações**.

## Figuras
| Figura sugerida | Arquivo |
|--|--|
| Camadas da arquitetura no fluxo da venda rápida | [../classes-0-camadas.png](../classes-0-camadas.png) |
| Classes — Acesso e notificações | [classes-1-acesso.png](classes-1-acesso.png) |
| Classes — Cadastros de pessoas e localidade | [classes-2-cadastros.png](classes-2-cadastros.png) |
| Classes — Produto, variações e preço | [classes-3-produto.png](classes-3-produto.png) |
| Classes — Classificação e fornecimento do produto | [classes-4-classificacao.png](classes-4-classificacao.png) |
| Classes — Lojas, locais, saldo e livro-razão | [classes-5-estoque.png](classes-5-estoque.png) |
| Classes — Transferência de estoque | [classes-6-transferencia.png](classes-6-transferencia.png) |
| Classes — Vendas e promoções | [classes-7-vendas.png](classes-7-vendas.png) |
| Classes — Pedidos de compra | [classes-8-compras.png](classes-8-compras.png) |
| Classes — Previsão: análise e recomendação | [classes-9-previsao-analise.png](classes-9-previsao-analise.png) |
| Classes — Previsão: aplicação da recomendação | [classes-10-previsao-aplicacao.png](classes-10-previsao-aplicacao.png) |
| Classes — Dados derivados para a previsão | [classes-11-dados-derivados.png](classes-11-dados-derivados.png) |
| Enumerações do domínio (página deitada) | [classes-12-enumeracoes.png](classes-12-enumeracoes.png) |

Legenda no Word: "Figura N – Diagrama de classes (Módulo). Fonte: Elaborado pelo autor (2026)."
A figura das camadas substitui a antiga "Representação estrutural das camadas da Clean Architecture".

## Como ler (texto para pôr abaixo da figura ou falar na banca)
- **Cor = módulo**, a mesma do DER. Classe de outro módulo aparece só com o nome e "ver <módulo>".
- **Nome da classe em inglês** (como no código) e, em itálico, o nome em português.
- **Atributos:** `+ Nome : Tipo` (`?` = aceita nulo; `{readOnly}` = calculado). As chaves estrangeiras não aparecem
  como atributo: viram as **associações** (linhas).
- **Operações:** construtores e métodos públicos de negócio (`Send`, `Receive`, `ApplyPurchase`, `Expire`...).
  Sublinhado = método estático. Parâmetros só com o nome, para caber; o tipo aparece quando há sobrecarga.
- **Associações:** multiplicidade nas pontas (`1`, `0..1`, `*`) e o nome da navegação no código (`Items`, `Variant`).
  **Losango cheio = composição** (a parte não existe sem o todo: itens da venda, variações do produto, locais da loja).
  Seta = navegação de um lado só. Linha tracejada = dono polimórfico (endereço e contato de cliente **ou** fornecedor).
- **Nota em cada figura:** todas as classes herdam de `BaseModel` (Id, CreatedAt) e têm `set` privado: o estado só
  muda pelo construtor e pelos métodos (encapsulamento; regras de negócio dentro da entidade).

## Roteiro para a banca
1. **Camadas (figura 0):** o controller só chama o caso de uso; o caso de uso orquestra; a regra fica na entidade;
   a infraestrutura implementa as interfaces do domínio. Todas as setas apontam para o domínio.
2. **Entidade rica:** `PurchaseOrder.Send/Receive/Cancel`, `ForecastRecommendation.ApplyPurchase/Dismiss/Expire`,
   `Promotion.Reschedule/Cancel`: o ciclo de vida está nos métodos, não em `set` público.
3. **Composição × associação:** a venda é dona dos itens e pagamentos; a promoção só *é aplicada* ao item.
4. **Estoque pelo livro-razão:** `StockMovement` nunca muda; `StockBalance.Apply` só soma movimentos.

## Como estes diagramas foram montados (método reaproveitável)
1. **Fonte = entidades do código**, não o banco: o diagrama de classes mostra comportamento (métodos), que o banco
   não tem. O [`gerar_classes.py`](gerar_classes.py) lê os `.cs` com expressões regulares:
   - propriedade pública → atributo; `virtual X` → associação 1 ou 0..1; `virtual ICollection<X>` → associação *;
   - `Guid XId` com navegação `X` → some como atributo (vira a linha);
   - construtores e métodos públicos (assinatura em várias linhas é juntada) → operações;
   - propriedade com `=>` → `{readOnly}`; `static` → sublinhado;
   - enums lidos de `Enums/*.cs`, com os valores fora do escopo do TCC escondidos.
2. **O que é decisão de modelagem fica em dicionários no script:** `COMPOSITIONS` (quais coleções são composição),
   `PT` (nome em português), `POLYMORPHIC`, `HIDDEN_ENUM_VALUES`. O script falha se aparecer classe sem módulo.
3. **Mesmo recorte e mesmas cores do DER**, para o leitor reconhecer o módulo de uma figura para a outra.
4. **Enumerações numa figura própria:** dentro de cada módulo elas ocupavam um terço da figura e puxavam setas de
   dependência; o tipo já aparece no atributo.
5. **A figura de camadas é feita à mão** (um fluxo real, venda rápida), com as classes e métodos conferidos no código.
6. **Revisar olhando a imagem** e ajustar: largura, linhas cruzadas, sobrecargas ambíguas.

### Truques de PlantUML específicos de classes
| Problema | Solução |
|--|--|
| Figura larga demais por causa dos enums | Enums numa figura só, empilhados por módulo com `-[hidden]down-` |
| Nome de `package` com "." vira pacotes aninhados | Não usar ponto no nome ("Nextflow Domain", não "Nextflow.Domain") |
| Duas sobrecargas iguais ("Client(dto)" duas vezes) | Mostrar os tipos dos parâmetros só quando a assinatura repete |
| Cor por módulo sem aparecer o estereótipo | `skinparam class<<modulo>> {...}` + `hide <<modulo>> stereotype` |
| Ícone de atributo (cadeado/bolinha) poluindo | `skinparam classAttributeIconSize 0` |

## Como gerar de novo
Nesta pasta (o script acha a API em `../../../../../../../nextflow`; outro caminho: `--code <pasta>`):
```bash
python3 gerar_classes.py
docker run --rm -u "$(id -u):$(id -g)" -e JAVA_TOOL_OPTIONS="-Duser.home=/tmp -DPLANTUML_LIMIT_SIZE=8192" \
  -v "$PWD/../..:/data" -w /data/classes/codigo plantuml/plantuml:1.2024.7 -tpng -charset UTF-8 classes-*.puml
```
