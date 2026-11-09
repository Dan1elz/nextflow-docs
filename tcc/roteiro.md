# Roteiro da refatoração do TCC

> **Status:** rascunho / a validar · **Data:** 2026-11-09 · **Arquivo:** `tcc/tcc.odt` (um arquivo só; o histórico fica no git)
> **Regra:** cada mudança entra como alteração controlada (autor "Claude (revisão TCC)"); o Daniel aceita ou recusa no editor.

## Estado
| Parte | Estado |
|--|--|
| Cap. 1 a 3 | Ajustes pontuais feitos (commit `481f488`), aguardando revisão do Daniel |
| Cap. 4 Desenvolvimento | A fazer (roteiro abaixo) |
| Cap. 5 Resultados | A fazer |
| Cap. 6 Considerações finais | A fazer |
| Resumo, abstract, listas, folha de aprovação | Por último |

### O que mudou nos cap. 1 a 3 (resumo para a revisão)
- 1: o "painel de controle de usuários" saiu do problema, da hipótese, do objetivo geral, de um objetivo específico e da
  justificativa; no lugar entra o apoio à decisão de compra (previsão de demanda). Público: comércios de pequeno e médio porte.
- 2.1 e 2.9: .NET 8 → .NET 10 (também no sumário e na referência, com acesso em 09 nov. 2026); "Machine Learning" saiu;
  Oracle VM → servidor virtual privado em provedor de nuvem (sem citar a Contabo); item novo de armazenamento compatível com S3.
- 2.7: só o papel Administrador nesta versão; perfis restritos ficam para depois (ADR 0004). As citações de RBAC e ANPD ficaram.
- 3.2: frase nova sobre as regras de negócio com código, fonte e data.
- 3.4: Kanban no Trello e depois no quadro versionado; Sprint 3 sem "futuro"; **Sprint 4 nova** (reestruturação e
  inteligência de compras). A Sprint 2 manteve o .NET 8, porque é histórico.
- **Fora, por decisão do Daniel (09/11):** declaração do uso de IA no desenvolvimento (ele fala com o orientador esta semana).

## Capítulo 4 — Desenvolvimento (proposta de estrutura)
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

## Capítulo 5 — Resultados
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
