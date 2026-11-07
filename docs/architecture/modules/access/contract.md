# Contrato — Acesso

> **Status:** implementado na F0.4, a validar · **Atualizado:** 2026-10-30 · Convenções: `../../contracts/README.md`
> Regras: `business-rules.md` (RN-AC*, RN-AC06..14 vindas de L-AC1..5, das decisões de 29/10 e da F0.4), decisão 0004 (só Admin) e RN-CE13 (só a visão do Admin).

## T-AC1. Login (`/login`)
Campos: e-mail, senha. O formulário exige só presença: o formato do e-mail é validado pela API (422 no campo).
Credencial errada: "E-mail ou senha inválidos." (401, RN-AC03). Usuário inativo com a senha certa: "Usuário inativo." (403, RN-AC02).
Após o login o front guarda o token. Ao recarregar, chama `/me`. A última loja usada fica no `localStorage` do navegador (RN-AC11).
Sem recuperação de senha nesta versão (`overview.md`).
```ts
POST /api/auth/login   LoginRequestDto → LoginResponseDto          // anônimo
GET  /api/auth/me      → CurrentUserDto
LoginRequestDto      { email; password }
LoginResponseDto     { token: string; expiresAt: string; user: CurrentUserDto }
CurrentUserDto       { id; name; lastName; email; role: Role; stores: CurrentUserStoreDto[] }
CurrentUserStoreDto  { id; name; locationCount }                   // só lojas ativas de user_stores; locationCount = locais ativos (seletor, RN-CE12)
```
Token vencido, inválido ou de usuário inativado: 401 sem corpo em qualquer rota autenticada, e o front encerra a sessão (RN-AC10).

## T-AC2. Usuários — listagem (`/users`)
Carrega: nome completo, e-mail, CPF (mascarado), perfil, ativo, criado em, último acesso. Filtros: `search` (nome, sobrenome, e-mail), `isActive`.
Ordenação aceita: `fullName`, `email`, `createdAt`, `lastLoginAt`.
Ações: novo, visualizar, editar, inativar/reativar. Usuário inativo não pode ser editado (400); reative antes.
Não permite inativar a si mesmo nem o último Admin ativo (RN-AC07): a API recusa com 400 e a tela nem oferece inativar a própria linha.
```ts
GET    /api/users?offset&limit&filters&sort&order → PaginationDto<UserListItemDto>
DELETE /api/users/{id}             → 204   // inativa
PATCH  /api/users/{id}/reactivate  → 204
UserListItemDto { id; fullName; email; cpfMasked; role: Role; isActive; createdAt; lastLoginAt? }
```

## T-AC3. Usuário — criar / editar / visualizar (`/users/create`, `/users/:id/edit`, `/users/:id/view`)
Campos: nome, sobrenome, CPF, data de nascimento, e-mail, senha (só na criação; na edição, campo "nova senha" opcional),
perfil (fixo "Administrador" e desabilitado enquanto só existir Admin, RN-AC04). E-mail e CPF únicos (RN-AC01), com erro no campo.
O CPF não muda depois de criado: na edição ele aparece desabilitado e não vai no DTO.
```ts
GET  /api/users/{id} → UserResponseDto
POST /api/users      UserRequestDto → 201 UserResponseDto
PUT  /api/users/{id} UpdateUserRequestDto → UserResponseDto
UserRequestDto       { name; lastName; cpf; birthDate: DateOnly; email; password }
UpdateUserRequestDto { name; lastName; birthDate: DateOnly; email; newPassword? }
UserResponseDto      { id; name; lastName; cpf; birthDate; email; role: Role; isActive; createdAt; updatedAt?; lastLoginAt? }
```

## T-AC4. Meu perfil (`/profile`, no menu do usuário)
Ver e editar os próprios dados (nome, sobrenome, e-mail) e trocar senha (senha atual + nova + confirmação; a confirmação é só do formulário).
A nova senha precisa ser diferente da atual. Senha atual errada: 422 no campo `currentPassword`. Tema claro/escuro (local).
```ts
PUT  /api/auth/me              UpdateProfileRequestDto → CurrentUserDto
POST /api/auth/change-password ChangePasswordRequestDto → 204
UpdateProfileRequestDto  { name; lastName; email }
ChangePasswordRequestDto { currentPassword; newPassword }
```

## Enums
`Role` trafega como string: `Admin` (`User` sem uso enquanto vigorar a decisão 0004).

## Lacunas encontradas neste módulo (fechadas em 2026-10-30, viraram regra em `business-rules.md`)
- **L-AC1** Rotas de autenticação em `/api/auth`, fora de `/api/users` → RN-AC06.
- **L-AC2** Não inativar a si mesmo nem o último Admin ativo → RN-AC07.
- **L-AC3** Senha com mínimo de 8 caracteres, letra e número (máximo de 100) → RN-AC08.
- **L-AC4** Token de 8 h, sem refresh token nem "lembrar-me" → RN-AC09.
- **L-AC5** `lastLoginAt` gravado a cada login com sucesso → RN-AC12.
