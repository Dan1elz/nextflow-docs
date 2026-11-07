# Módulo Acesso — visão

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-30
> **Origem:** `nextflow/docs/PROJECT.md` (UsersController, JWT), F0.4 (`AuthController`, `UsersController`), TCC (RF004, quadros 3 e 4), decisões R2 e R6 do review

## O que faz hoje
Login por e-mail e senha com token JWT; cadastro, edição, inativação e reativação de usuários. O código tem os papéis
`User` e `Admin`, mas a decisão vigente é usar só Admin (decisão global 0004).

## Fora do módulo por enquanto
Recuperação de senha (citada no TCC, não implementada), refresh token, perfis/permissões por módulo, times, auditoria.

## Perguntas em aberto
- Recuperar senha entra na versão do TCC? Sem e-mail transacional, como? (Hoje não entra: as telas foram removidas na F0.4, 2026-10-30.)
