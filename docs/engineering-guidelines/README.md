# Padrões de engenharia — princípios comuns

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** `CLAUDE.md` dos repositórios, conversa de 27/10/2026 sobre o estilo de trabalho, modelo do projeto Aura.

O padrão de código de cada stack fica **no próprio repositório**:

| Repositório | Guideline | Entrada para agentes | Setup |
|--|--|--|--|
| `../nextflow` (API .NET) | `docs/C_SHARP_ARCHITECTURE_RULES.md`, `docs/dotnet-development-guidelines.md`, `docs/DOMAIN_LEVELS.md` (padrão atrena, ADR 0010) | `AGENTS.md` | `docs/local-setup.md` |
| `../nextflow-front` (React) | `docs/engineering-guidelines.md` + skill `.agents/skills/shadcn/` | `AGENTS.md` | `docs/local-setup.md` |

## Princípios comuns
- Siga o código ao lado. Padrão novo precisa de motivo; se for estrutural, de uma decisão registrada em `architecture/decisions/`.
- Qualidade de dev pleno, com design patterns, mesmo com o código escrito majoritariamente por IA.
- Português no que o usuário lê e na documentação; inglês no código.
- Regra de negócio nova ou alterada nasce no `business-rules.md` do módulo (com fonte e data) antes do código.
- Erros explicam o motivo em linguagem de negócio ("Estoque insuficiente para…"), não em termos técnicos.
- Integrações tolerantes a falha: timeout, nova tentativa limitada, log do erro e caminho alternativo (ex.: previsão sem IA).
- Nada de segredo em código, log ou documentação.
- Testes, quando existirem, levam no nome o ID da regra (`RN-*`) que verificam.
- Git: `main` estável; trabalho em branch `task-NN`; commits pequenos com contexto; commit e push só com o ok do Daniel.
