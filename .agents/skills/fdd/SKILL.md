---
name: fdd
description: Entrevista para desenhar uma feature (Feature Design Document) antes de codar; use quando surgir uma funcionalidade nova ou mudança de regra relevante em um módulo do Nextflow.
---

# FDD por entrevista

Saída: `docs/architecture/modules/<módulo>/features/AAAA-MM-DD-<titulo>.md` (vira o changelog do módulo) e as regras e
decisões que a feature cria.

## Roteiro
1. Problema: quem sofre, em que momento, com que frequência. Qual regra atual (`RN-*`) é afetada.
2. Resultado esperado: como saber que funcionou (critério de aceite verificável).
3. Fluxo principal e alternativos (passo a passo do usuário e do sistema).
4. Regras: liste cada uma com ID novo; aponte conflito com regras e decisões existentes.
5. Fora do escopo: o que esta feature não faz.
6. Impacto técnico: API, front, banco (migration), integrações, previsão.
7. Testes: quais casos, nomeados pelos IDs das regras.

## Template do arquivo
```
# AAAA-MM-DD — Título
> Status: proposta | em desenvolvimento | entregue · Módulo: · Regras: RN-…
## Problema
## Critérios de aceite
## Fluxo
## Regras
## Fora do escopo
## Impacto técnico
## Testes
```
Não comece a implementação antes de o Daniel validar o FDD.
