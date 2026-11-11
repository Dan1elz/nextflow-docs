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
| 5 | 4.9.5 Medição da precisão | MAPE: venda zero, exclusão por ruptura, venda observada × demanda, 15% como meta | aprovado (11/11) | 2151518 |
| 6 | 4.10.1 Acessibilidade | Evidências medidas: WCAG, contraste, teclado, foco, leitores de tela, auditoria | aprovado (11/11) | 6db78a6 |
| 7 | 5.1 Resultados obtidos | Dados simulados: método, parâmetros, datas, distribuição, ruptura, lotes, semente, repetição | aprovado (11/11) | 7d05684 |
| 8 | 5.1 Resultados obtidos | Validação da previsão: funcionamento × acurácia; regra-base se viável | aprovado (11/11) | 7d05684 |
| 9 | 5.2 Testes automatizados | Evidências: comando, versão, data, ambiente, relatório; separar 1.059 back × 84 front | aprovado (11/11) | 74ec08c |
| 10 | 5.3 Desempenho | Mesma máquina, sem rede nem concorrência; ferramenta; não extrapolar; p95, dispersão, máximo, erros | aprovado (11/11) | 74ec08c |
| 11 | 4.9.3 Papel da IA | Regras de validação: justificar 50–150%, revalidação (estoque, mínimo, múltiplo, prazo, orçamento), autorização do gestor | aprovado (11/11) | 2a32725 |
| 12 | 4.3 Requisitos | Rastreabilidade RF/RNF → casos de uso → testes; onde estão os 52 casos de uso | aprovado (11/11) | 658b8e5 |
| 13 | 5.2.3 Avaliação heurística | Avaliadores, roteiro, problemas, severidade, correções; inspeção interna ≠ teste com usuários | aprovado (11/11) | ae6feb3 |
| 14 | 5.3 Discussão sobre os resultados | Qualificar objetivos; separar implementação, testes internos e validação externa pendente | aprovado (11/11) | 2822769 |
| 15 | 6 Considerações finais | Generalização: sem estudo de implantação, custo ou lojistas; tratar como potencial do protótipo | aprovado (11/11) | efc9ad5 |

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

## 6. 4.10.1 Acessibilidade

**Parágrafo comentado:** o parágrafo único do 4.10.1 (shadcn/ui, "contraste adequado nos dois temas").

**Comentário:**
> ESSENCIAL | ACESSIBILIDADE: trazer evidências mensuráveis (critérios WCAG, relação de contraste, navegação por
> teclado, foco, leitores de tela ou auditoria automatizada/manual). Uso de shadcn/ui e afirmação de "contraste adequado"
> não demonstram, por si só, conformidade ou acessibilidade validada.

**Texto do colega:** correto no tom (shadcn não garante conformidade, WCAG 2.2 como referência), mas todo no
condicional ("deve considerar", "permitem documentar"), sem nenhum número. Não foi usado como base.

**Medição (11/11/2026):** `tcc/ferramentas/contraste.py` lê os tokens OKLCH de `nextflow-front/src/index.css`, converte
para sRGB e aplica a razão de contraste da WCAG. Primeira medição: abaixo do mínimo a mensagem de erro no claro (4,4),
o texto do botão principal e os links no escuro (3,9 e 4,4), o botão de exclusão no escuro (2,8), o anel de foco (2,2)
e a borda dos campos (1,3).

**Correção no front** (branch `fix/contraste-wcag` do nextflow-front, **sem commit**, aguardando o Daniel validar nas
telas): `--destructive` claro mais escuro; `--input` opaco e mais escuro nos dois temas; `--ring` opaco; no escuro,
`--primary` mais claro com texto escuro (`--primary-foreground`) e `--destructive-foreground` escuro; `ring-ring/50`
virou `ring-ring` em button, calendar e item, e `outline-ring/50` virou `outline-ring`. Depois: todos os pares passam
(menor: borda dos campos no escuro, 3,3:1). Build ok, 84 testes ok, lint sem erro novo (53 erros antigos em outros
arquivos).

**Outras evidências levantadas:** `lang="pt-BR"`; 56 `aria-invalid` e `aria-describedby` no `form.tsx`; 93 `aria-label`;
16 `sr-only`; 153 consultas por papel/rótulo nos testes contra 1 por test id; componentes Radix.

**O que foi feito no TCC:** 4.10.1 reescrito (introdução, contraste com o novo Quadro 15 de antes/depois, teclado e
foco, leitores de tela, testes, limitações); quadros 15–17 viraram 16–18; a WCAG 2.2 entrou nas referências (W3C, 2023)
e passou a ser citada no capítulo 2; o RNF da interface troca "contraste adequado" pelos mínimos 4,5:1 e 3:1.

**Pontos ligados, ainda sem mexer:**
- Auditoria com axe ou Lighthouse e teste com leitor de tela (exigem o navegador; o texto assume como limitação).
- Cores dos gráficos não medidas.
- Prints do TCC com o tema escuro mostram o roxo antigo dos botões; refazer se o Daniel aprovar as cores.

## 7 e 8. 5.1 Resultados obtidos (dados simulados e validação da previsão)

**Parágrafos comentados:** os três parágrafos da 5.1 (sistema entregue, dados de demonstração, análise de 08/11).

**Comentários:**
> ESSENCIAL | DADOS SIMULADOS: documentar método e parâmetros de geração dos 36 meses, datas especiais, distribuição das
> vendas, indisponibilidade, lotes, semente aleatória (se houver) e scripts ou critérios de repetição; separar claramente
> dados sintéticos de resultados reais.

> ESSENCIAL | VALIDAÇÃO DA PREVISÃO: as recomendações coerentes com padrões inseridos em dados sintéticos demonstram
> funcionamento, não acurácia preditiva em uso real. Explicitar essa distinção e, se viável, comparar com regra-base ou
> cenários controlados independentes.

**Como o seed funciona** (`nextflow.Infrastructure/Seeders/Demo`: `DemoDemand.cs`, `DemoHistorySimulation.cs`,
`DemoHistorySeeder.cs`, `DemoScenariosSeeder.cs`):
- Demanda/dia = volume mensal × fator do mês (14 perfis) × fator de evento (Páscoa, Namorados, Mães, Pais, Crianças,
  Natal) × dia da semana (0,55 dom. a 1,35 sáb.) × tendência (1,08/ano estável, 1,45 crescente, 0,70 decrescente) × 0,8.
  Data única (ovo, kits) só na janela de 21 a 42 dias. Segunda loja = 60%. Venda do dia ~ Poisson (normal acima de 30).
- Reposição a cada 14 dias por fornecedor e loja, mirando prazo + 14 + 28 dias; prazo real = cadastrado −2 a +3 dias;
  custo ±3%. Venda limitada ao saldo do salão (ruptura = venda perdida). Lote por chegada de alimento, validade = vida
  útil; saída FEFO pelo livro-razão.
- Semente fixa 42 (`RandomSeed`), âncora gravada na nota da abertura; `Seed:Demo:HistoryMonths` = 36. Testes:
  `DemoHistorySeedTests`, `DemoScenariosSeedTests`.
- **Cenários inseridos:** `LateLastOrder` em 6 produtos (DP-003, 008, 017 trufa, 021 panetone, 041, 046) corta a última
  reposição; recebimento de ontem com lotes de 12 e 25 dias; transferência "errada" Shopping → Centro. As 6 compras, 2
  promoções e 4 transferências da análise de 08/11 vêm desses cenários.

**O que foi feito:** a 5.1 manteve o 1º parágrafo; o 2º virou quatro (dados sintéticos, modelo de demanda, reposição/
ruptura/lotes, cenários inseridos e repetição); o 3º passou a ligar cada recomendação ao cenário que a provocou e ganhou
um parágrafo que separa funcionamento de acurácia (cita regra-base como forma de avaliar com dados reais). Também
ajustados com fundo verde: resumo, abstract (que ainda dizia "only prioritizes and explains", sobra dos itens 2/4),
discussão, limitações e conclusão.

**Enxugado (11/11, pedido do Daniel):** os seis parágrafos novos da 5.1 viraram quatro (dados sintéticos; simulação e semente; cenários e resultado da análise; funcionamento × acurácia), sem os parâmetros finos (fatores do dia da semana, ±3% de custo, 28 dias de cobertura), que ficam só aqui no controle. Resumo e abstract com a frase mais curta.

**Ponto em aberto:** comparação com regra-base em cenário controlado (backtest na simulação: prever cada um dos últimos
12 meses com o histórico até o mês anterior e comparar o MAPE com "mesmo mês do ano anterior" e "média dos 3 últimos
meses"). Não feito; depende do ok do Daniel (código novo no back).

## 9. 5.2 Testes automatizados

**Comentário:**
> RECOMENDADO | EVIDÊNCIAS DE TESTES: indicar comando, versão do código, data, ambiente e onde consultar relatório/log de
> execução. Distinguir explicitamente 1.059 testes de backend dos 84 testes de frontend e esclarecer se todos os 84 também
> foram executados/aprovados.

**Execução nova (11/11/2026)**, relatórios em `docs/evidencias/2026-11-11/`:
- Back: `dotnet test nextflow.Tests --logger trx`, versão `8b410cf` (homolog), 1.062 testes (617 unidade + 445
  integração; +3 do contrato do payload da IA), todos aprovados, 11 min 6 s. `testes-back.trx` e `testes-back-console.txt`.
- Front: `npx vitest run --reporter=junit`, versão `aba7f64` (homolog, com as cores WCAG), 84 testes em 17 arquivos,
  todos aprovados, 16 s. `testes-front-junit.xml` e `testes-front-console.txt`.
- Ambiente: máquina de desenvolvimento, WSL 2 (kernel 6.6), .NET SDK 10.0.103, Node 24.14, Vitest 3.2.7, Docker 29.2.
- O TRX só tem nomes de teste com "Password", sem senha nem token (conferido).

**O que foi feito:** o parágrafo da 5.2 virou dois; o segundo separa as suítes ("não se somam"), dá comando, versão,
data, tempo, ambiente e a pasta dos relatórios. Resumo e abstract: 1.059 → 1.062.

## 10. 5.3 Desempenho

**Comentário:**
> ESSENCIAL | DESEMPENHO: deixar claro que medições ocorreram na mesma máquina (API+BD), sem latência de rede externa nem
> carga concorrente. Descrever ferramenta de medição e condições, e evitar extrapolar a média para VPS/produção. Se
> possível, incluir p95, dispersão ou máximos e taxa de erros.

**Pedido do Daniel (11/11):** medir na VM, não no local. A VM foi atualizada (back `8b410cf`, front `aba7f64`, `git pull
--ff-only` + `docker compose -f compose.homolog.yaml up -d --build` em `~/projects/nextflow-v2/`).

**Medição:** `tcc/ferramentas/medir_desempenho.sh` reescrito (curl, 1 aquecimento + 100 requisições sequenciais por rota,
saída com erros, média, desvio, p50, p95 e máximo). Duas rodadas em 11/11/2026, com o banco de homologação (42 produtos,
67.674 movimentações, 20.785 vendas):
- Interna, 19:46: na VM contra o IP do contêiner da API (sem rede externa). VM: 4 vCPU AMD EPYC, 7,8 GB, Ubuntu 24.04,
  compartilhada com outros projetos (load 1 a 2). `desempenho-homolog-interno.tsv`.
- Pública, 19:55: do computador de desenvolvimento para `https://dev-nextflow-api.zanni.tech` (internet, proxy, TLS).
  `desempenho-homolog-publico.tsv`.
- 0 erros em 1.400 requisições. Pior caso interno 839 ms (faturamento 12 meses); público 1,8 s (listagem de produtos).
  Medianas públicas ~250 ms acima das internas.
- Uma primeira rodada interna logo após o rebuild (load 4) foi descartada.

**O que foi feito:** o parágrafo da 5.3 virou dois (ambiente e condições; ferramenta e as duas medições); o Quadro 17
foi refeito com média, p95 e máximo das duas medições; a análise depois do quadro passou a citar 0 erros, os máximos, a
diferença da rede e que vale para um usuário por vez. Resumo e abstract trocaram "menos de 100 ms" por "até 1,8 s no
servidor de homologação". O desvio padrão e a p50 estão nos TSV, não no quadro.

## GitHub (pedido do Daniel junto com os itens 9 e 10)

O TCC só dizia "repositório GitHub" (3.x, rastreabilidade). Agora cita os três repositórios públicos
(`github.com/Dan1elz/nextflow`, `-front`, `-docs`) e que servem para reproduzir os testes e as medições. **Os commits do
nextflow-docs precisam estar no GitHub** para os links das evidências valerem.

## Extra: uso de IA no projeto (pedido do Daniel, 11/11/2026)

Não é comentário do orientador. Nova subseção **3.3.3 Uso de inteligência artificial no desenvolvimento**, com entrada no
sumário (página aproximada) e referências ANTHROPIC (Claude Code) e OPENAI (ChatGPT).
- Respostas do Daniel: só o Claude Code no código; na etapa final, ChatGPT só para dúvidas de documentação; declarar
  também o apoio na revisão do texto do TCC.
- Evidência: commits com `Co-Authored-By: Claude` até 11/11/2026: back 70/197, front 76/194, docs 61/66 (desde 26/10 no
  código e 07/11 nos docs).
- ABNT: não há norma oficial confirmada que obrigue a declaração (NBR 6023 e 10520 não tratam de IA generativa); declarar é
  a prática recomendada pelas bibliotecas. Conferir se a Fatec tem regra própria.

## 11. 4.9.3 Papel da IA (regras de validação)

**Comentário:**
> RECOMENDADO | REGRAS DE VALIDAÇÃO: justificar a faixa de 50% a 150% e como os ajustes da IA são revalidados contra
> estoque, pedido mínimo, múltiplo, prazo e limite orçamentário; indicar se existe autorização explícita do gestor sobre o
> valor ajustado.

**Base:** versão revisada pelo grupo (quatro etapas, 50–150% como restrição sem validação estatística, valor final pode
sair da faixa, prazo do cálculo, sem limite orçamentário, autorização do gestor).

**Conferido no código:** `ForecastGuardrails` (clamp e depois `AdjustPurchase` com vida útil, mínimo e múltiplo;
`Deadline = calc.Deadline`); `ForecastActionUseCases` (aplicar Comprar gera pedido em Orçamento, nada é enviado; avisos de
mínimo, múltiplo e validade são do diálogo e não bloqueiam); `apply-purchase-dialog.tsx` (quantidade editável, avisos,
custo estimado do pedido); `forecast-detail.tsx` (selo de ajuste da IA e quantidade calculada ao lado); RN-VD13
(promoção abaixo do custo exige confirmação). O prompt (regra 3) mostra a intenção da faixa: a IA só muda a quantidade
diante de evento comercial, validade ou cobertura curta.

**Ajustes sobre a versão do grupo:** justificativa da faixa (antecipar ou reduzir sem mudar a ordem de grandeza);
autorização detalhada (diálogo editável com avisos e custo, pedido em orçamento que ainda precisa ser enviado, confirmação
de promoção abaixo do custo) no lugar de "validações correspondentes"; tirada a frase "Em qualquer caso, a recomendação
só produz efeito..." porque o item de autorização já diz isso. Rótulo do 4º item: "Persistência e autorização".

## 12. 4.3 Requisitos (rastreabilidade)

**Comentário:**
> RECOMENDADO | RASTREABILIDADE: incluir (ou indicar onde existe) matriz RF/RNF → casos de uso → testes/resultado. São
> mencionados 52 casos de uso, mas somente quatro estão especificados em detalhe e os requisitos funcionais estão
> agrupados; indicar onde os demais são documentados.

**O que foi feito:**
- `tcc/ferramentas/rastreabilidade.py` lê os relatórios de 11/11 (TRX do back, JUnit do front) e gera
  `docs/architecture/rastreabilidade.md`: RF → casos de uso → classes/arquivos de teste com contagem; RNF → verificação.
  Os 52 UC se dividem entre os 12 RF sem sobra; 1.010 testes do back e 80 do front ficam ligados aos RF, e 52 + 4
  cobrem infraestrutura, migrações e seed. Zero falhas.
- TCC: parágrafo novo na 4.3 (onde estão os 52 UC e as regras; Apêndice B; arquivo da matriz) e **Apêndice B – Matriz de
  rastreabilidade dos requisitos** com o **Quadro 19** (no fim, para não renumerar os quadros), com entrada no sumário e
  no índice de ilustrações.
- Ponto fraco visível na matriz: RF012 (painel e notificações) tem só 2 testes de backend; o front cobre com 19.

## 13. 5.2.3 Avaliação heurística

**Comentário:**
> RECOMENDADO | USABILIDADE: informar quantos avaliadores, roteiro, problemas encontrados, severidade e correções feitas.
> A análise pelos próprios desenvolvedores é uma inspeção interna, não substitui testes com usuários independentes.

Não há registro da avaliação nos docs (o roteiro só diz "sem teste com usuários, decisão do Daniel, 09/11"). Material para
os problemas encontrados: commits `fix` do front de 06 a 11/11 (≈20 correções de interface, várias vindas da conferência
de telas do Daniel) e o contraste do item 6.

**Respostas do Daniel (11/11):** ninguém além dos três usou o app; sem roteiro formal ("fui abrindo e testando"); item
opcional; pode usar as correções do histórico como problemas.

**O que foi feito:** o parágrafo de abertura virou: método (três integrantes, sem roteiro, telas dos fluxos principais nos
dois temas e no celular, de 06 a 11/11, escala de gravidade de Nielsen de 0 a 4), lista de seis problemas com heurística,
gravidade e correção (commits `71a0faf`, `07f9093`, contraste do item 6, `bc58b38`, `ac6cb93`, `e3127f0`) e um parágrafo
final com o Quadro 18 e a ressalva de inspeção interna. Sem quadro novo, para não renumerar.


## 14. 5.3 Discussão sobre os resultados

**Comentário:**
> ESSENCIAL | CONCLUSÕES: qualificar o alcance dos objetivos. Segurança e acessibilidade não tiveram verificação completa
> descrita; a precisão da demanda ainda não possui observações reais, e a usabilidade não foi testada com usuários.
> Separar implementação, testes internos e validação externa pendente.

**Versão do colega:** boa direção (limitações, validação real como próxima etapa), mas genérica ("foram realizadas
verificações de acessibilidade") e sem separar os três níveis. Não foi usada como base.

**O que foi feito:** os três parágrafos da 5.3 viraram três níveis: (1) implementação, com os objetivos alcançados nesse
nível; (2) verificação interna com os números (1.062 + 84 testes, Apêndice B, homologação, WCAG, inspeção da equipe) e
"não equivalem a uma validação externa"; (3) validação externa pendente em quatro pontos (precisão sem dado real;
usabilidade e acessibilidade sem usuários, tecnologias assistivas nem auditoria; segurança sem teste de invasão; carga
concorrente não medida) e as limitações de escopo (um perfil, previsão da empresa). Nos trabalhos futuros, o item
"validação em uso real" passou a incluir a apresentação da prova de conceito aos comerciantes, auditoria de
acessibilidade, leitores de tela, análise de vulnerabilidades e testes de carga (fecha os pontos ligados dos itens 1 e 6).

## 15. 6 Considerações finais

**Comentário:**
> RECOMENDADO | GENERALIZAÇÃO: não há estudo de implantação, custo total ou avaliação com lojistas para comprovar
> acessibilidade econômica e benefícios operacionais. Apresentar como potencial do protótipo até haver evidência de adoção
> real.

**Versão do colega:** bem qualificada ("potencial de aplicação", "dependem de avaliações específicas"), mas reescrevia
todos os parágrafos num tom mais genérico e menos de produto. Aproveitei as ideias e mantive o texto original onde ele
não generaliza (problema do lojista e diferencial).

**O que foi feito:**
- Parágrafo dos dados de demonstração: "dados sintéticos", "histórico simulado", "situações que, numa operação real,..." e
  "mostra o comportamento esperado do sistema, mas não comprova sua eficácia em um comércio real".
- Parágrafo do dia a dia: "busca simplificar"; "ferramenta acessível" virou "potencial do protótipo"; nova frase de que
  o potencial não foi comprovado (sem estudo de implantação, custo total nem avaliação com lojistas).
- Parágrafo da equipe: "sistema funcional e testado" virou "protótipo funcional, verificado por testes automatizados e
  por simulações".
- Trabalhos futuros: a validação em uso real inclui levantar o custo de implantação e os ganhos na operação.
- Mesma generalização em outros lugares: resumo e abstract ("ferramenta acessível" → protótipo com potencial que depende
  de validação com lojistas) e fim da justificativa ("necessidades reais das empresas modernas" → "necessidades apontadas
  pelas pesquisas sobre pequenos negócios"; ponto ligado do item 1).
- O parágrafo "No dia a dia", que já estava verde de antes desta revisão, foi reescrito e segue verde.

## Fechamento (11/11/2026)

Todos os 15 comentários aprovados. Depois disso:
- **Listas de figuras e de quadros** viraram campos do Word (`TOC \z \c "Figura"` e `\c "Quadro"`), sem `\h`, então sem
  link azul. As 64 legendas voltaram a ter o campo `SEQ` (tinham perdido nas conversões). O `settings.xml` ganhou
  `updateFields`: ao abrir, o Word pergunta se atualiza os campos; responder **Sim** acerta as páginas das listas e do sumário.
- **Simplificações** (com fundo verde para leitura): justificativa (parágrafo técnico e o "Em suma"), 3.3 e 3.3.1 (dois
  parágrafos genéricos sobre metodologia ágil e sprints), 4.1 (o 2º parágrafo repetia a 4.9.3; virou duas frases e uma
  remissão) e a última frase do parágrafo da LGPD na 4.9.3.
- A busca por repetição literal (blocos de 5 a 7 palavras) só achou citações do NIC.br, que ficaram.

## Checklist final
- [x] Todos os itens da tabela aprovados
- [ ] Pontos ligados ainda abertos (não bloqueiam a entrega):
  - ADR 0005 no nextflow-docs ainda diz "só prioriza e explica" (alinhar com RN-DF22 e com a 4.9.3);
  - prints do tema escuro no TCC mostram o roxo antigo dos botões (refazer com as cores WCAG);
  - termos da API gratuita do Gemini (decidir se o TCC menciona);
  - exemplo de payload com dados do seed como apêndice (opcional);
  - comparação da previsão com regra-base na simulação (opcional, não feita);
  - cores dos gráficos não medidas.
- [x] Fundo verde retirado do documento inteiro
- [x] Referências novas em ordem alfabética e citadas no texto (Sebrae 2023, W3C, Anthropic, OpenAI; conferido em 11/11)
