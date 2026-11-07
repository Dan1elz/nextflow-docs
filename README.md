# Nextflow — documentação do produto

Repositório de documentação do **Nextflow**, um micro ERP para gestão de produtos e vendas com inteligência de compras
(previsão de demanda sazonal). É a fonte de verdade do **produto** (o que ele faz, por quê e com quais regras).
O código mora nos repositórios irmãos:

| Pasta | Conteúdo |
|--|--|
| `../nextflow` | API (.NET 8, Clean Architecture) |
| `../nextflow-front` | SPA (React 19 + TypeScript) |
| `./` (esta) | Documentação de produto, arquitetura, padrões e processos |

> ⚠️ **Estado atual (28/10/2026):** tudo aqui é **rascunho / a validar**. O conteúdo foi extraído do código, dos docs dos
> repositórios, do texto do TCC e do review de outubro/2026, mas o produto vai mudar. Nada vira verdade antes de ser
> validado com o Daniel na etapa de entrevistas. Cada documento informa a própria origem.

## Mapa

```
docs/
├── product-overview.md              visão do produto (devs e QAs)
├── implementation-plan.md          plano de implementação por fases e fatias (até a banca)
├── architecture/
│   ├── architecture-overview.md     HLD: módulos, infraestrutura, integrações
│   ├── business-rules.md            regras que valem para o produto inteiro
│   ├── decisions/                   decisões do produto inteiro (ADR numerado)
│   ├── modules/<módulo>/            overview, business-rules, decisions, features, third-parties
│   ├── integrations/                contrato de cada integração de terceiro
│   └── diagrams/                    diagramas (Mermaid)
├── engineering-guidelines/          só princípios comuns; o padrão de cada stack fica no repo
└── process/                         deploy, onboarding, setup local, incidentes
AGENTS.md                            regras para agentes de IA que editam esta pasta
.agents/skills/                      prompts de entrevista: prd, hld, fdd, c4, mermaid
```

## Status dos documentos

| Status | Significado |
|--|--|
| `rascunho / a validar` | Extraído de fonte existente ou proposto; não confirmado |
| `decidido (rascunho)` | O Daniel já decidiu, mas a redação ainda não foi revisada |
| `validado` | Revisado e confirmado com o Daniel, com data |
| `obsoleto` | Substituído (indicar por qual documento) |

## Fontes usadas na primeira versão

- `../nextflow/CLAUDE.md`, `../nextflow/docs/PROJECT.md`, `AI_FORECAST_SPEC.md`, `FILTERS.md`, `DOCKER.MD`
- `../nextflow-front/CLAUDE.md`, `../nextflow-front/docs/PROJECT.md`, `diagramas.md`, `DOCKER.md`
- Texto do TCC (ABNT v9) e diagrama de visão de produto (Excalidraw), ambos de 2026
- Review de código e QA de 27/10/2026 (doc "Nextflow — achados e decisões do review")
