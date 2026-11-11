# Comentários do orientador

Versão comentada: `Nextflow - TCC - Formatado - 10_11_2026 - Copiar.docx`. Os comentários chegam um a um, porque o
arquivo não traz os comentários do Word. Cada item entra no `tcc/tcc.docx` com fundo verde até o Daniel aprovar; depois
o fundo sai e passamos ao próximo.

**Status:** pendente · em revisão (no docx, com fundo verde) · aprovado (fundo retirado)

| # | Seção | Comentário (resumo) | Status | Commit |
|--|--|--|--|--|
| 1 | 3.2 Levantamento de requisitos | Detalhar a modelagem de processos e as histórias de usuário; validação | aprovado (11/11) | 05305ef |
| 2 | 4.1 Visão geral do sistema | Contradição: "todos os números são determinísticos" × IA "refina quantidade ou desconto" (4.9.3) | aprovado (11/11) | ec88a7a |
| 3 | 4.9.3 Papel da IA | Privacidade: mostrar os campos do payload ao Gemini e como são filtrados (LGPD) | aprovado (11/11) | 5675448 |
| 4 | 4.9.3 Papel da IA | Contradição com 4.1, 4.5.2, resumo e conclusão; documentar campos alteráveis, antes/depois e salvaguardas | aprovado (11/11) | 3ac0ce5 |
| 5 | 4.9.5 Medição da precisão | MAPE: venda zero, exclusão por ruptura, venda observada × demanda, 15% como meta | em revisão | 2151518 |

## 1. 3.2 Levantamento de requisitos

**Parágrafo comentado:**
> Para a extração das necessidades do sistema, empregou-se a técnica de Modelagem de Processos de Negócio, permitindo o
> mapeamento das rotinas essenciais de controle, desde o ingresso de mercadorias via fornecedores até o fluxo de saída
> para o cliente final. A definição do escopo foi operacionalizada por meio de User Stories (Histórias de Usuário),
> garantindo que o desenvolvimento fosse orientado pela entrega de valor contínuo e pela priorização de demandas reais
> do fluxo logístico.

**Comentário:**
> ESSENCIAL | LEVANTAMENTO: detalhar como se realizou a modelagem de processos e a elaboração das histórias de usuário:
> fontes, participantes, documentos, instrumentos e critérios de priorização. Indicar se as necessidades foram validadas
> por lojistas reais ou definidas pela equipe.

**O que foi feito:** o parágrafo virou cinco: (1) equipe de três autores, sem comerciantes, com pesquisa documental e
análise de concorrentes (Omie, Bling); (2) mapeamento Sebrae/CDL-BH com 1.334 MPE; (3) fluxos, regras de negócio,
registros de decisão e casos de uso; (4) priorização por dependência entre módulos e prazo; (5) hipóteses não validadas
com lojistas, sistema como prova de conceito. As menções a BPMN e a histórias de usuário saíram, porque não houve esse
processo formal (os cards do Trello são tarefas técnicas). Referência nova: Agência Sebrae de Notícias (2023).

**Respostas do Daniel (11/11/2026):** sem BPMN formal, os diagramas são os do nextflow-docs; nenhum comerciante
consultado; priorização por dependência e prazo; concorda em assumir a prova de conceito e a validação como próxima etapa.

**Pontos ligados, ainda sem mexer** (aguardando para ver se o orientador comentou neles):
- 3.1 Análise de cenário: "observação prática do cenário" pode se apoiar na pesquisa e nos concorrentes.
- Fim da justificativa: "necessidades reais das empresas" → "necessidades apontadas pelas pesquisas".
- Trabalhos futuros: incluir a apresentação da prova de conceito aos lojistas.
- Resumo (opcional): de onde vieram os requisitos.

## 2. 4.1 Visão geral do sistema

**Parágrafo comentado:**
> O princípio que orienta esse módulo é a divisão de papéis entre o servidor, a inteligência artificial e o gestor:
> todos os números da previsão são produzidos por cálculo determinístico no backend; a inteligência artificial apenas
> prioriza e explica as recomendações, dentro de limites definidos; e nenhuma ação é executada sem a decisão do gestor.
> Assim, cada sugestão pode ser conferida e reproduzida, e o sistema continua funcionando mesmo sem o serviço de
> inteligência artificial.

**Comentário:**
> ESSENCIAL | CONSISTÊNCIA INTERNA: seção 4.9.3 diz que o Gemini pode "refinar a quantidade ou o desconto". Aqui se
> afirma que todos os números são determinísticos e que a IA apenas prioriza/explica. Esclarecer se o resultado final
> pode mudar numericamente; distinguir cálculo base, ajuste da IA, regras de validação e valores persistidos, inclusive
> no resumo e na conclusão.

**Como funciona de fato** (código `ForecastGuardrails.cs`, `ForecastRecommendation.cs`; RN-DF10 a 12, 22, 25, 29):
- Sim, o resultado final pode mudar numericamente. A IA pode trocar a prioridade e propor quantidade (0,5× a 1,5× da
  necessidade, depois pedido mínimo, múltiplo e vida útil), desconto (5% até o máximo da margem) e dias de promoção (7 a 45).
- Valor fora da faixa é levado ao limite, e o motivo registra o ajuste. A IA não muda a confiança, não cria Comprar,
  Promover ou Transferir sem o gatilho do cálculo, e não troca uma compra urgente por Manter.
- Ficam gravados: o valor final (`SuggestedQuantity`, desconto, dias), a `CalculatedQuantity`, o `ReasonCalculated`
  ao lado do motivo da IA e o `AiAdjusted`. O desconto calculado não é gravado à parte.
- O gestor ainda edita quantidade, desconto e período nos diálogos de aplicar.

**O que foi feito:**
- 4.1: o parágrafo virou dois (o que o cálculo produz, o que a IA pode ajustar, a validação, o que é gravado, a decisão do gestor).
- 4.9.3 Papel da IA: virou uma lista com as quatro etapas (cálculo base, ajuste da IA, regras de validação, valores persistidos) e o comportamento na falha.
- Arquitetura (princípio "o servidor calcula, a IA interpreta"), resumo e conclusão: só o trecho sobre a IA foi trocado.

**Pontos ligados, ainda sem mexer:**
- ADR 0005 no nextflow-docs ainda diz "só prioriza e explica"; atualizar para casar com RN-DF22.
- "Assim, cada sugestão pode ser reproduzida" saiu: a resposta da IA não é reproduzível, só o cálculo.

## 3. 4.9.3 Papel da inteligência artificial (privacidade)

**Parágrafo comentado:** os dois parágrafos do 4.9.3 (versão de 10/11), terminando em "Nenhum dado pessoal de clientes
é enviado ao serviço."

**Comentário:**
> ESSENCIAL | PRIVACIDADE: apresentar quais campos compõem o payload enviado ao Gemini e como são filtrados/anonimizados.
> A afirmação é relevante para LGPD e não deve permanecer apenas declaratória; citar testes, estrutura de integração ou
> exemplo sem dados reais.

**Texto proposto pelo colega:** payload com identificador e informações comerciais do produto, saldos, pedidos pendentes,
preços, prazos, vendas mensais agregadas, índices sazonais e recomendações calculadas; princípio da necessidade (LGPD art.
6º, III); sem vendas individuais nem dados de clientes.

**Validação contra o código** (`ForecastAiPrompt.BuildPayload`, `BuildSummaryPayload`, `ForecastProductInput`,
`OnDemandSuggestionUseCases`, `GeminiAiClient`):
- Correto no geral. Ajustes: "pedidos pendentes" na verdade é só a quantidade a chegar somada, não os pedidos; faltavam
  validade, promoção vigente, desconto máximo, demanda projetada, cobertura, confiança, eventos comerciais e fora de linha.
- Faltavam também a chamada de resumo (contagens e até 15 recomendações) e a sugestão sob demanda (nome da loja, do local
  e código do lote).
- Não há anonimização: os dados pessoais nunca entram, porque `ForecastProductInput` não tem campo de cliente ou usuário e
  as vendas chegam agregadas por produto e mês.
- **Não existe teste** que trave os campos do payload. Os testes do orquestrador cobrem só ordenação e leitura da resposta.

**O que foi feito:** a frase "Nenhum dado pessoal..." saiu do parágrafo da falha. Entrou um parágrafo de abertura, a lista
com os seis grupos de campos, um parágrafo sobre o resumo e a sugestão sob demanda e um parágrafo da LGPD (art. 6º, III,
Brasil 2018, que já estava nas referências), com a filtragem pela estrutura e a chave só no cabeçalho.

**Pontos ligados, ainda sem mexer:**
- ~~Teste de contrato do payload~~ feito no back (branch `test/payload-ia-lgpd`, ainda sem commit): `ForecastAiPayloadTests`
  (lote, resumo e a entrada da previsão sem campo de cliente) e checagem nos dois testes RN-DF30 da sugestão sob demanda,
  com a lista em `Tests/Support/AiPayloadContract.cs`. O 4.9.3 cita os testes no fim do parágrafo da LGPD.
- O total de testes do capítulo 5 (1.059 no back) vai mudar: 3 testes novos. Atualizar quando a suíte for rodada de novo.
- Exemplo de payload com dados do seed, como apêndice ou figura.
- Termos da API gratuita do Gemini: o Google pode usar o conteúdo enviado para melhorar os produtos. Os dados de
  produto, preço e custo são comerciais, não pessoais, mas vale decidir se o TCC menciona isso.

## 4. 4.9.3 Papel da inteligência artificial (transparência)

**Parágrafo comentado:** o primeiro parágrafo do 4.9.3 (versão de 10/11), com "a IA pode ajustar a prioridade, refinar a
quantidade ou o desconto".

**Comentário:**
> ESSENCIAL | IA GENERATIVA: resolver a contradição com seções 4.1, 4.5.2, resumo e conclusões, que atribuem à IA apenas
> priorização/explicação. Documentar campos alteráveis, valores antes/depois e salvaguardas, para garantir transparência
> do mecanismo de decisão.

**O que já estava resolvido pelo item 2:** 4.1, 4.5.2 (princípio "o servidor calcula, a IA interpreta"), resumo,
conclusão e a lista das quatro etapas no 4.9.3.

**Sobras achadas na varredura:**
- Justificativa (cap. 1): "utiliza a inteligência artificial apenas para priorizar e explicar".
- Quadro 1, RF da previsão: "com priorização e explicação por inteligência artificial".
- UC39 "Priorizar e explicar com a IA" (especificação do UC38 e diagrama da Figura 7).

**O que foi feito:**
- As três sobras foram corrigidas. O UC39 virou "Revisar com a IA dentro dos limites"; o diagrama `uc-7-previsao.puml`
  foi gerado de novo e trocado no docx (imagem não tem fundo verde).
- 4.9.3: novo **Quadro 14 – Campos da recomendação que a IA pode alterar** (campo, valor de origem, o que a IA pode
  fazer, salvaguarda, o que fica gravado) e um exemplo de antes/depois: compra 100 → IA 200 → gravado 150, com a nota
  do código; desconto 20% calculado → IA 30% → gravado 23% (preço R$ 10, custo R$ 7, margem de 10%).
- Quadros 14, 15 e 16 viraram 15, 16 e 17 (legendas, índice e citações). A entrada nova do índice está sem hiperlink e
  com página aproximada: atualizar o índice no Word na formatação final.

**Conferido no código:** `ForecastGuardrails.cs` (ação, prioridade, quantidade, desconto, dias, notas no motivo),
`ForecastCalculator.cs` (desconto sugerido 5–25%, promoção 14–30 dias, margem 1,10 sobre o custo).

## 5. 4.9.5 Medição da precisão

**Parágrafo comentado:** o parágrafo único do 4.9.5 (versão de 10/11).

**Comentário:**
> ESSENCIAL | MAPE: explicar tratamento dos meses com venda real igual a zero (divisão por zero), critérios de exclusão
> por ruptura e distinção entre vendas observadas e demanda verdadeira. Descrever se 15% é meta interna e não resultado
> já medido.

**Texto proposto pelo colega:** fórmula do erro mensal, exclusão de venda zero com previsão positiva, 0% quando os dois
são zero, exclusão por ruptura em mais da metade dos dias, 15% como critério interno, viés de ±5%.

**Validação contra o código** (`ForecastAccuracyCalculator.cs`, `ForecastProjectionRepository.GetAccuracyRows`,
`DerivedDataCalculator.MonthlySales`; RN-DF19, RN-DF26):
- Tudo confere com o código: erro = |previsto − vendido| ÷ vendido × 100; venda 0 com previsão > 0 sai (`NoSales`);
  os dois zerados contam 0%; ruptura quando dias sem estoque × 2 > dias do mês (`Stockout`); viés acima de +5% ou abaixo
  de −5%; tolerância MAPE ≤ 15% (RN-DF26, decidido em 08/11, antes 20%).
- A projeção de referência é a da última análise concluída (com ou sem IA) com data de referência antes do dia 1º do mês.
- Dia sem estoque = soma do fechamento das variações nos locais vendáveis ≤ 0.
- O indicador geral é a % de produtos dentro da tolerância entre os que têm algum mês medido.
- O sistema estima a demanda perdida por ruptura (RN-CE24), mas a medição usa a venda registrada, não a demanda estimada.

**O que foi feito:** o parágrafo virou três, com fundo verde: (1) como a comparação é feita e a fórmula; (2) venda zero,
ruptura e venda observada × demanda verdadeira, incluindo o limite da exclusão (ruptura parcial ainda distorce);
(3) 15% como critério interno da equipe, o indicador geral, o viés e o fato de ainda não haver medição (remete às limitações).

## Checklist final
- [ ] Todos os itens da tabela aprovados
- [ ] Pontos ligados resolvidos ou descartados
- [ ] Fundo verde retirado do documento inteiro
- [ ] Referências novas em ordem alfabética e citadas no texto
