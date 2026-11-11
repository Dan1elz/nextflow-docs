# Roteiro da refatoração do TCC

> **Status:** rascunho / a validar · **Data:** 2026-11-09 · **Arquivo:** desde 09/11 (tarde) o que vale é o DOCX do Daniel
> (`Downloads/Nextflow - TCC - Formatado.docx`, cópia versionada em `tcc/tcc.docx`). O `tcc.odt` e o `montar.sh` ficam
> como histórico de como os capítulos foram gerados; edições novas vão direto no DOCX (ex.: `ferramentas/ajustar_docx.py`).
> **Regra:** cada mudança entra como alteração controlada (autor "Claude (revisão TCC)"); o Daniel aceita ou recusa no editor.
> Todo texto novo também leva **fundo verde** (estilo `TccNovo`) para a leitura. O verde não some ao aceitar a alteração:
> antes da entrega, rodar `python3 -I tcc/ferramentas/limpar_destaque.py tcc/tcc.odt`.
>
> **Ferramentas** (`tcc/ferramentas/`): `odtrack.py` aplica uma lista de trocas (`ops_*.py`) como alterações controladas;
> `odt2txt.py` extrai o texto (com as alterações aceitas) para conferir; `limpar_destaque.py` tira o verde.
> Sempre aplicar sobre a versão anterior commitada e comparar o texto antes de gravar.

## Estado
| Parte | Estado |
|--|--|
| Cap. 1 a 3 | Ajustes pontuais feitos (commit `481f488`), aguardando revisão do Daniel |
| Cap. 4 Desenvolvimento | Reescrito por inteiro (44 figuras, 13 quadros), aguardando revisão; fonte em `ferramentas/cap4.py` |
| Cap. 5 Resultados | Reescrito por inteiro (Quadros 14 a 16), aguardando revisão; fonte em `ferramentas/cap5.py` |
| Cap. 6 Considerações finais | Reescrito com foco no produto (pedido do Daniel, 09/11), aguardando revisão; fonte em `ferramentas/cap6.py` |
| Resumo, abstract, listas, sumário, apêndice | Feitos por `ferramentas/pretextuais.py` (último passo do `montar.sh`), aguardando revisão |

### O que mudou nos cap. 1 a 3 (resumo para a revisão)
- 1: o "painel de controle de usuários" saiu do problema, da hipótese, do objetivo geral, de um objetivo específico e da
  justificativa; no lugar entra o apoio à decisão de compra (previsão de demanda). Público: comércios de pequeno e médio porte.
- 2.1 e 2.9: .NET 8 → .NET 10 (também no sumário e na referência, com acesso em 09 nov. 2026); "Machine Learning" saiu;
  Oracle VM → servidor virtual privado em provedor de nuvem (sem citar a Contabo); item novo de armazenamento compatível com S3.
- 2.7: só o papel Administrador nesta versão; perfis restritos ficam para depois (ADR 0004). As citações de RBAC e ANPD ficaram.
- 3.4: Kanban "inicialmente no Trello e, posteriormente," no quadro versionado; Sprint 3 sem "futuro"; **Sprint 4 nova**
  (inteligência de compras e consolidação), em que o backend "foi atualizado para a versão 10 do .NET". A Sprint 2 manteve
  o .NET 8.
- **Fora, por decisão do Daniel (09/11):** declaração do uso de IA no desenvolvimento (ele fala com o orientador esta semana)
  e a frase da 3.2 sobre regras levantadas em entrevistas.
- **Regra para todo o texto (Daniel, 09/11):** a banca não conhece versão anterior, então nada de "reestruturação",
  "escopo redefinido" ou "nova versão"; mudança vira evolução natural ("posteriormente", "foi atualizado"). E o texto não
  pode dar a entender que o Daniel é dono ou responsável pelo produto: o trabalho é da equipe.

## Capítulo 4 — Desenvolvimento
O capítulo é gerado de `ferramentas/cap4.py` por `ferramentas/gerar_capitulo.py` (troca o capítulo inteiro, numera
figuras e quadros, embute as imagens e marca tudo em verde). Correção de texto: editar o `cap4.py` e regerar sobre a
versão commitada. Como o capítulo inteiro é novo, ele não usa alteração controlada; o texto antigo fica no git (`12fbc09`).

**Pendências do cap. 4 (09/11)**
- Figura `seq-3-compra`: cita RN-CP02 em "sem recebimento parcial"; o certo é RN-CP04 (Quadro 3). Regerar a imagem.
- Print da precisão (`13-previsao-precisao`) está vazio ("Ainda sem meses medidos"): ficou fora; precisa de print com dados.
- Print da previsão (`10-previsao`) é a página inteira e, para caber na folha, fica com letra pequena: melhor um recorte da tela.
- RN-DF30 está no Quadro 3, mas a regra ainda está "a aprovar".
- Nova referência: GOOGLE, Gemini API documentation (citada em 4.5 e 4.9).
- Sumário, listas de figuras e quadros e o Apêndice A ficam para a etapa dos pré-textuais; os quadros do cap. 5 precisam ser renumerados (começam no 14).

### Estrutura aprovada para o cap. 4 (proposta original)
| Seção | Conteúdo | Fonte |
|--|--|--|
| 4.1 Visão geral | Micro ERP com inteligência de compras; "o backend calcula, a IA interpreta, o humano decide" | `product-overview.md`, ADR 0001, 0005 |
| 4.2 Módulos e funcionalidades | Acesso, Cadastros, Catálogo e estoque, Vendas, Compras, Inteligência de compras | `product-overview.md` §5, `modules/*/overview.md` |
| 4.3 Requisitos | Quadro de RF novo (por módulo); quadro de RNF quase igual (.NET 10) | `modules/*/business-rules.md`, RNF do HLD |
| 4.4 Casos de uso | 8 figuras por escopo (UC01–UC52) + 4 quadros de especificação (login, venda rápida, gerar análise, aplicar Comprar) | `diagrams/uml/casos-de-uso/` |
| 4.5 Arquitetura | Camadas (figura `classes-0-camadas`), decisões principais: estoque como livro-razão, variação como unidade, lojas e locais | ADR 0007, 0008, 0009, 0010 |
| 4.6 Modelo de domínio | 7 diagramas de classe por módulo; completo no apêndice | `diagrams/uml/classes/` |
| 4.7 Modelo de dados | DER por módulo (11) + geral no apêndice; dicionário só das tabelas centrais no corpo, completo no apêndice | `diagrams/uml/der/`, `der/esquema` |
| 4.8 Sequência | 7 fluxos (login e painel, venda rápida, compra, estoque, análise, aplicar Comprar, sugestão da IA) | `diagrams/uml/sequencia/` |
| 4.9 Previsão de demanda | **Seção central**: dados derivados, cálculo, sazonalidade, guardrails, papel da IA, ações, precisão | `modules/demand-forecast/*`, `integrations/gemini.md` |
| 4.10 Interfaces | ~10 telas mais importantes (abaixo) | `docs/screenshots/light/` |

### Telas propostas (claro; uma de celular no fim)
`00-login`, `01-painel`, `50-produtos` ou `52-produto-visualizar`, `57-movimentacoes`, `20-venda-rapida`,
`30-pedidos-compra`, `10-previsao`, `11-previsao-detalhe`, `13-previsao-precisao`, `70-lojas-e-locais`, `mobile/20-venda-rapida`.

### Referências novas prováveis (só entram com fonte conferida)
- Documentação da API do Google Gemini (seção 4.9).
- Opcional: Amazon S3 (só se o texto citar o padrão S3 como fonte).

## Montagem
`ferramentas/montar.sh` refaz o `tcc.odt` do zero: original (`12fbc09`) → ajustes dos cap. 1 a 3 (`ops_cap1a3.py`, alterações
controladas) → cap. 4 (`cap4.py`) → cap. 5 (`cap5.py`). Qualquer correção vai nos arquivos-fonte e o documento é remontado.
Se o Daniel editar o `tcc.odt` à mão, commitar antes e levar a edição para a fonte, senão a próxima montagem a perde.

## Capítulo 5 — feito em 09/11
- Sem teste com usuários (decisão do Daniel, 09/11): a verificação virou testes automatizados (Quadro 14, 19 cenários,
  cada um com teste aprovado na suíte), medição de tempo de resposta (Quadro 15) e avaliação heurística de Nielsen (Quadro 16).
  O objetivo específico do cap. 1 foi ajustado ("testes automatizados, medições de tempo de resposta e avaliação heurística").
- Suíte do back em 09/11: 1.059 casos (614 unidade, 445 integração), todos aprovados, 10 min 36 s. Front: 84 testes (Vitest).
- Desempenho medido em 09/11 com `ferramentas/medir_desempenho.sh` numa API isolada (Postgres temporário na porta 56543,
  banco novo com o seed: 42 produtos, 67.809 movimentações, 20.838 vendas; Ryzen 7 5700X, 16 GB), 20 execuções por rota.
  Análise sem IA: 17 s para 42 produtos. O Postgres de dev não sobe enquanto o `pgsql-averba-replica` ocupa a porta 5435.

### Proposta original do cap. 5
- Quadro 25 (testes funcionais): preencher com cenários cobertos pelos testes automatizados de integração (mais de 1.000 testes).
- Quadro 26 (desempenho, RNF003): medir no ambiente com o seed de 36 meses (listagem de produtos, kardex, painel, análise).
- Precisão da previsão: números da tela `/forecast/accuracy` com o seed (tolerância de ±15%, RN-DF26).
- Usabilidade (SUS): depende de aplicação com usuários; fica marcado para o Daniel.
- Discussão: inverter o "a previsão ainda não foi implementada".

## Capítulo 6 — Considerações finais
- Objetivo alcançado com a previsão implementada; trabalhos futuros: perfis restritos, previsão por loja
  (`ideas/pos-tcc-previsao-por-loja.md`), financeiro, NF-e, multi-tenant (ADR 0003), orçamento (F2.5).

## Elementos pré-textuais (no fim)
- Resumo e abstract novos; palavras-chave (incluir previsão de demanda e inteligência artificial).
- Listas de figuras, quadros e siglas (novas: ADR, FEFO, LLM, S3, VPS) e o sumário, que são texto manual.
- Folha de aprovação com "Americana, 18 de junho de 2021" (sobra do modelo): data da banca.

## Pré e pós-textuais — feito em 09/11
- Resumo, abstract e palavras-chave novos; folha de aprovação com "Americana, ___ de dezembro de 2026." (preencher a data).
  Os nomes da banca (Benedito, Renato, Antonio) e a dedicatória vieram do modelo: **confirmar com o orientador**.
- Listas de figuras (45) e quadros (16) e o sumário (62 títulos) são gerados das legendas e dos títulos do documento.
  O sumário é um índice de verdade: no Word, clicar nele e "Atualizar sumário" para pôr os números de página.
- Siglas: só as que aparecem no texto (tabela em `pretextuais.py`).
- Apêndice A virou "Mapa geral do modelo de dados" (Figura 45, `der-apendice-geral.png`).
- Referências: a ABNT NBR 10520:2023 está na lista, mas não é citada no texto (decidir se fica).
- O `montar.sh` recusa gravar o `tcc.odt` se ele estiver aberto (arquivo `~$` na pasta); dá para montar em outro caminho:
  `./montar.sh /caminho/saida.odt`.
