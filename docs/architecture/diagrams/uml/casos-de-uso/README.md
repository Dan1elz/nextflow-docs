# Diagramas de casos de uso

> **Status:** rascunho para o TCC, gerado em 09/11/2026 a partir do código atual (controllers da API e telas); aguarda
> revisão do Daniel. Fonte em PlantUML (`*.puml`, estilo em `../estilo.iuml`); PNG a 200 dpi para o Word.

Uma figura por módulo, para caber numa página. Os códigos (UC01…) servem para o texto citar o caso de uso.

## Por que PlantUML e não Mermaid
O `AGENTS.md` pede Mermaid, mas o Mermaid não tem diagrama de casos de uso UML (ator, fronteira do sistema,
`<<include>>` e `<<extend>>`). Os diagramas antigos simulavam isso com fluxograma. Aqui vale a exceção da regra 7
("imagem só quando Mermaid não der conta"): o `.puml` é texto versionável e o PNG é gerado dele.

## O que mudou em relação aos diagramas antigos
- **Um ator humano só, o Administrador** (ADR 0004). O "Operador" saiu.
- **Atores de sistema:** o **Agendador** (análise semanal e resumo diário de alertas) e o **Serviço de IA** (Gemini).
- **Saíram** "Elaborar orçamento" e "Estornar/Cancelar venda": o pedido com orçamento (F2.5) e o reembolso (F2.6)
  ficaram fora do escopo. Também saiu "Gerar relatório de recolhas", que não existe no sistema.
- **Entraram:** lojas e locais, lotes e validade, transferência, política ABC, promoções, previsão com IA (Comprar,
  Promover, Transferir, Descartar), precisão, painel e notificações.

## Figuras
| Figura sugerida | Arquivo |
|--|--|
| Diagrama de casos de uso — Acesso e segurança | [uc-1-acesso.png](uc-1-acesso.png) |
| Diagrama de casos de uso — Cadastros de pessoas | [uc-2-cadastros.png](uc-2-cadastros.png) |
| Diagrama de casos de uso — Catálogo de produtos | [uc-3-catalogo.png](uc-3-catalogo.png) |
| Diagrama de casos de uso — Estoque | [uc-4-estoque.png](uc-4-estoque.png) |
| Diagrama de casos de uso — Vendas e promoções | [uc-5-vendas.png](uc-5-vendas.png) |
| Diagrama de casos de uso — Compras | [uc-6-compras.png](uc-6-compras.png) |
| Diagrama de casos de uso — Previsão de demanda com IA | [uc-7-previsao.png](uc-7-previsao.png) |
| Diagrama de casos de uso — Painel e notificações | [uc-8-painel.png](uc-8-painel.png) |

Legenda no Word: "Figura N – Diagrama de casos de uso (Módulo). Fonte: Elaborado pelo autor (2026)."

## Descrição dos casos de uso
Todos exigem autenticação (UC01), exceto o próprio UC01.

| UC | Caso de uso | Ator | Descrição | Regras |
|--|--|--|--|--|
| UC01 | Autenticar-se | Administrador | Entra com e-mail e senha e recebe um token de acesso. | RN-AC02, RN-AC03 |
| UC02 | Manter o próprio perfil e trocar a senha | Administrador | Altera nome e e-mail e troca a senha informando a atual. | — |
| UC03 | Gerenciar usuários | Administrador | Cadastra, edita e consulta usuários (todos Administradores). | ADR 0004 |
| UC04 | Ativar ou desativar usuário | Administrador | Desativa sem apagar; usuário inativo não entra. | RN-AC02 |
| UC05 | Selecionar a loja de trabalho | Administrador | A loja do topo filtra painel, listas, estoque e o novo pedido de compra. | ADR 0001 (previsão) |
| UC06 | Gerenciar clientes | Administrador | Cadastro completo com endereços e contatos; desativar e reativar. | RN-CD* |
| UC07 | Cadastrar cliente rápido | Administrador | Nome e CPF sem sair da venda de balcão. | RN-CD* |
| UC08 | Gerenciar fornecedores | Administrador | Cadastro com CNPJ, prazo de entrega, endereços e contatos. | RN-CD* |
| UC09 | Manter endereços | Administrador | Endereço com país, estado e cidade (IBGE). | — |
| UC10 | Manter contatos | Administrador | Telefone e/ou e-mail (pelo menos um). | — |
| UC11 | Consultar compras do cliente ou do fornecedor | Administrador | Vendas do cliente e pedidos de compra do fornecedor. | — |
| UC12 | Gerenciar produtos | Administrador | Produto com tipo, categoria, coleção, eventos, foto, preço e mínimos. | RN-CE* |
| UC13 | Manter variações | Administrador | Grade (tamanho, sabor, cor) com SKU, código de barras e preço por variação. | RN-CE34 |
| UC14 | Vincular fornecedores | Administrador | Fornecedor preferido, prazo, pedido mínimo e múltiplo de compra. | RN-CE27 |
| UC15 | Alterar ciclo de vida | Administrador | Em linha ou fora de linha (a data de lançamento é um campo do produto). | RN-CE19 |
| UC16 | Gerenciar categorias | Administrador | Árvore de 2 níveis. | — |
| UC17 | Gerenciar coleções | Administrador | Agrupa produtos (Páscoa, Natal…). | — |
| UC18 | Gerenciar calendário de eventos | Administrador | Datas comerciais com regra de recorrência e antecedência; alimentam a sazonalidade. | RN-DF* |
| UC19 | Gerenciar lojas e locais de estoque | Administrador | Lojas, locais (vendável ou não) e locais padrão de venda e recebimento. | ADR 0009 |
| UC20 | Definir política de estoque | Administrador | Cobertura alvo e segurança por classe ABC. | RN-DF* |
| UC21 | Consultar estoque por local e por lote | Administrador | Saldo por variação × local × lote, com validade. | RN-CE09, ADR 0008 |
| UC22 | Registrar ajuste ou perda | Administrador | Entrada ou saída manual com motivo. | RN-CE01, RN-CE14 |
| UC23 | Dar baixa em lote vencido | Administrador | Ajuste já preenchido a partir do lote. | RN-CE14 |
| UC24 | Transferir estoque entre locais | Administrador | Sai de um local e entra em outro, mantendo os lotes (FEFO). | RN-CE62 |
| UC25 | Consultar movimentações (kardex) | Administrador | Histórico de entradas e saídas com custo e saldo após. | RN-CE01 |
| UC26 | Realizar venda rápida | Administrador | Venda de balcão já paga; baixa o estoque pelo livro-razão. | RN-VD02, RN-VD05, RN-VD16 |
| UC27 | Buscar item por nome, SKU ou código de barras | Administrador | Inclusive por leitor de código de barras. | — |
| UC28 | Registrar pagamentos | Administrador | Uma ou mais formas; a soma fecha o total. | RN-VD05, RN-VD18, RN-VD20 |
| UC29 | Consultar histórico de vendas | Administrador | Lista com filtros e o detalhe de cada venda. | — |
| UC30 | Gerenciar promoções | Administrador | Desconto por período para o produto ou uma variação; edita só a agendada; cancela. | RN-VD13 |
| UC31 | Confirmar promoção abaixo do custo | Administrador | Exigida quando o preço promocional fica abaixo do custo médio. | RN-VD13 |
| UC32 | Elaborar pedido de compra | Administrador | Pedido em orçamento por fornecedor, com local de entrega. | RN-CP07 |
| UC33 | Sugerir custo e regras do fornecedor | Sistema | Último custo, pedido mínimo e múltiplo ao incluir o item. | — |
| UC34 | Enviar pedido ao fornecedor | Administrador | Orçamento → Pendente, grava a data de envio. Nunca automático. | RN-CP08, RN-DF15 |
| UC35 | Receber pedido | Administrador | Recebe o pedido inteiro: entrada por item e custo médio atualizado. | RN-CP02, RN-CP04, RN-CE31 |
| UC36 | Informar lote e validade | Administrador | Só para produto que controla lote. | ADR 0008 |
| UC37 | Cancelar pedido | Administrador | Pedido recebido não cancela. | RN-CP03 |
| UC38 | Gerar análise de demanda | Administrador, Agendador | Em segundo plano, uma por vez; manual ou semanal. | RN-DF18, RN-DF23 |
| UC39 | Priorizar e explicar com a IA | Serviço de IA | Lotes sequenciais de produtos; a IA ajusta dentro dos limites. | RN-DF12, RN-DF13, RN-DF20 |
| UC40 | Consultar recomendações | Administrador | Lista por ação, prioridade e confiança, com o detalhe do cálculo. | RN-DF21 |
| UC41 | Aplicar Comprar | Administrador | Gera pedidos de compra em orçamento por fornecedor. | RN-DF15 |
| UC42 | Dividir a compra entre lojas | Administrador | Parte de cada loja pela falta dela, um pedido por loja. | RN-DF27, RN-DF28 |
| UC43 | Aplicar Promover | Administrador | Cria a promoção sugerida (uma ou várias). | RN-DF25 |
| UC44 | Aplicar Transferir | Administrador | Cria a transferência entre locais. | RN-DF16, RN-DF29 |
| UC45 | Descartar recomendação | Administrador | Com motivo. | — |
| UC46 | Consultar precisão da previsão | Administrador | Erro da projeção contra o vendido, por mês, produto, classe e categoria. | RN-DF19, RN-DF26 |
| UC47 | Configurar agendamento | Administrador | Dia, hora e tamanho do lote enviado à IA. | RN-DF18, RN-DF20 |
| UC48 | Acompanhar o painel | Administrador | Faturamento, margem, ticket, recomendações, gráfico e alertas. | — |
| UC49 | Ver estoque baixo e lotes vencendo | Administrador | Lista completa ("ver mais"), trocando a loja do topo para agir. | — |
| UC50 | Pedir sugestão de compra ou de desconto à IA | Administrador, Serviço de IA | Para qualquer item, dentro dos limites; abre o pedido ou a promoção preenchidos. | RN-DF30 (a aprovar) |
| UC51 | Receber notificações | Administrador | Sino com análise concluída e alertas. | RN-DF18, RN-DF23 |
| UC52 | Enviar resumo diário de alertas | Agendador | Estoque baixo e lotes vencendo do dia. | — |

## Como estes diagramas foram montados (método reaproveitável)
Roteiro usado aqui, que serve para qualquer sistema com API e telas.

### 1. Partir do que o sistema faz, não da memória
- **Fonte da verdade = código.** Listar os endpoints de cada controller (ou as rotas do front) e agrupar o que é a
  mesma intenção do usuário. Ex.: `GET/POST/PUT/DELETE /api/clients` + `PATCH reactivate` = "Gerenciar clientes".
  Comando usado: `grep -E '\[Http(Get|Post|Put|Patch|Delete)' -r Controllers/`.
- **Conferir o escopo** no quadro de fatias e nas decisões: o que foi cortado (aqui, orçamento, reembolso e
  inventário) **não entra**, mesmo que esteja no plano antigo.
- **Conferir os perfis** nas decisões de acesso: um ator por perfil real, não por cargo imaginado.

### 2. Escolher os atores
- **Humanos:** um por perfil de acesso (aqui, só o Administrador).
- **De sistema:** quem dispara algo sem clique (agendador, fila, webhook) e quem o sistema consulta por fora
  (IA, gateway de pagamento). Ficam do lado direito do diagrama; os humanos ficam à esquerda.

### 3. Recortar por escopo (uma figura por página)
- Um diagrama por módulo do produto, com **no máximo uns 8 casos de uso**. Passou disso, dividir (aqui, "Catálogo e
  estoque" virou duas figuras).
- O diagrama completo, se for preciso, vai só em apêndice.

### 4. Nomear e numerar
- Nome do caso de uso = **verbo no infinitivo + objeto**, do ponto de vista do ator ("Receber pedido", não "Recebimento").
- Numeração contínua (UC01…UC52) na ordem dos módulos, para o texto citar. Caso de uso que aparece em dois módulos
  mantém o mesmo número (UC07 e UC32 aparecem em mais de uma figura).

### 5. Usar `<<include>>` e `<<extend>>` com critério
- **`<<include>>`:** passo que **sempre** acontece dentro do outro e vale a pena mostrar
  (venda rápida → registrar pagamentos; receber pedido → lançar entrada no livro-razão).
- **`<<extend>>`:** comportamento **opcional ou condicional**, que nasce de dentro de outro caso de uso
  (dar baixa em lote vencido estende registrar ajuste; dividir entre lojas estende aplicar Comprar).
  A seta aponta **para o caso de uso estendido**.
- Não usar `include` para "estar logado": isso vira uma frase única ("todos exigem UC01").
- Não modelar CRUD em quatro casos de uso: "Gerenciar X" basta.

### 6. Deixar a figura limpa e levar o detalhe para o texto
- **Regras de negócio fora do desenho.** Notas com linhas longas poluem a figura; as regras vão na tabela de
  descrição (UC, nome, ator, descrição, regras), que o texto acadêmico já espera.
- Título dentro da figura e a fronteira do sistema nomeada ("Nextflow — Módulo").

### 7. Estilo para impressão (`../estilo.iuml`)
- Preto e branco, fonte sem serifa, fundo branco, `skinparam dpi 200` (nítido no Word e no PDF).
- `left to right direction` em casos de uso; atores humanos à esquerda, atores de sistema à direita.
- Um arquivo de estilo comum incluído com `!include ../estilo.iuml` em todos os diagramas.

### 8. Truques de layout do PlantUML (o que resolveu aqui)
| Problema | Solução |
|--|--|
| Setas de `extend` emboladas | Dar direção: `UC41 .up.> UC40 : <<extend>>` |
| Ator de sistema caindo embaixo do sistema | Inverter a seta: `UC52 <-- Agendador` põe o ator à direita |
| Linha longa atravessando a figura | Reordenar a declaração dos casos de uso ou usar `A -[hidden]- B` |
| Aspas aparecendo como `\"` | Não escapar aspas no rótulo; escrever sem aspas |
| Texto de nota virando título | Linha começando com `=` é título no Creole; reescrever a frase |
| Pasta `?` criada pelo Docker | Passar `-e JAVA_TOOL_OPTIONS=-Duser.home=/tmp` |

### 9. Revisar como o leitor vai ver
Gerar o PNG, **abrir e olhar** cada figura (cruzamento de linhas, texto cortado, legibilidade em meia página) e
iterar. Juntar todas numa folha só ajuda a ver a consistência entre elas.

### Modelo inicial
```plantuml
@startuml uc-modulo
!include ../estilo.iuml
left to right direction
title Casos de uso — Módulo

actor "Perfil humano" as Ator
actor "Sistema externo" as Ext

rectangle "Sistema — Módulo" {
  usecase "UC01 Gerenciar X" as UC01
  usecase "UC02 Passo sempre presente" as UC02
  usecase "UC03 Variação opcional" as UC03
  usecase "UC04 Consultar serviço externo" as UC04
}

Ator --> UC01
UC01 ..> UC02 : <<include>>
UC03 .up.> UC01 : <<extend>>
UC04 --> Ext
@enduml
```

## Como gerar as imagens
```bash
docker run --rm -u "$(id -u):$(id -g)" -e JAVA_TOOL_OPTIONS=-Duser.home=/tmp \
  -v "$PWD/..:/data" -w /data/casos-de-uso plantuml/plantuml:1.2024.7 -tpng -charset UTF-8 *.puml
```
(rodar dentro desta pasta)
