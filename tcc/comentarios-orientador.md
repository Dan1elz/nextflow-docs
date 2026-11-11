# Comentários do orientador

Versão comentada: `Nextflow - TCC - Formatado - 10_11_2026 - Copiar.docx`. Os comentários chegam um a um, porque o
arquivo não traz os comentários do Word. Cada item entra no `tcc/tcc.docx` com fundo verde até o Daniel aprovar; depois
o fundo sai e passamos ao próximo.

**Status:** pendente · em revisão (no docx, com fundo verde) · aprovado (fundo retirado)

| # | Seção | Comentário (resumo) | Status | Commit |
|--|--|--|--|--|
| 1 | 3.2 Levantamento de requisitos | Detalhar a modelagem de processos e as histórias de usuário; validação | aprovado (11/11) | 05305ef |
| 2 | 4.1 Visão geral do sistema | Contradição: "todos os números são determinísticos" × IA "refina quantidade ou desconto" (4.9.3) | em revisão | ec88a7a |

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

## Checklist final
- [ ] Todos os itens da tabela aprovados
- [ ] Pontos ligados resolvidos ou descartados
- [ ] Fundo verde retirado do documento inteiro
- [ ] Referências novas em ordem alfabética e citadas no texto
