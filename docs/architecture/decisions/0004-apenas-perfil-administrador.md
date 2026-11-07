# 0004 — Apenas o perfil Administrador por enquanto

> **Status:** decidido (rascunho) · **Data:** 2026-10-27 · **Quem decidiu:** Daniel
> **Origem:** decisão R2 do review de 27/10/2026

## Contexto
O código tem os papéis `User` e `Admin`, com regras de autorização inconsistentes (QA encontrou telas que o `User` vê mas
recebe 403). O TCC descreve Operador e Administrador.

## Decisão
Por ora só existe o perfil **Administrador**. Toda rota exige login. Permissões modulares (perfil × tabela × ação, escopo
de dados OWN/DEPARTMENT/GLOBAL) vêm depois, junto com o multi-tenant.

## Consequências
- O papel `User` deixa de ter uso (remover ou ignorar: a decidir na implementação).
- O texto do TCC precisa refletir isso ou justificar o Operador como futuro.
