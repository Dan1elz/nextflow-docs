# 0003 — Multi-tenant por schema, só como trabalho futuro

> **Status:** decidido (rascunho) · **Data:** 2026-10-27 · **Quem decidiu:** Daniel
> **Origem:** diagrama de visão de produto (entidades Companies, Modules, CompanyModules) e conversa de 27/10/2026

## Contexto
A visão de produto prevê várias empresas no mesmo sistema, com login pelo slug da empresa e módulos contratados.

## Decisão
Quando existir, o multi-tenant será **um schema do PostgreSQL por empresa**. Não entra na versão do TCC.
Antes de desenhar, estudar o projeto Aura do Daniel como referência (não agora).

## Consequências
- Hoje o banco é de uma empresa só; nenhuma tabela tem `CompanyId`.
- Vira item de "Trabalhos futuros" do TCC.
