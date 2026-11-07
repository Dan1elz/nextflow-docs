# Módulo Acesso — regras de negócio

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-30
> **Origem:** código da API (use cases de Users), decisões do review de 27/10/2026, lacunas L-AC1..5 do `contract.md`, decisões delegadas pelo Daniel em 29/10/2026

| ID | Regra | Fonte | Data | Status |
|--|--|--|--|--|
| RN-AC01 | E-mail e CPF de usuário são únicos; o erro volta no campo (422) | `UserConfiguration` (índices únicos), `CreateUserUseCase` | 2026-10-30 | implementado |
| RN-AC02 | Usuário inativo não consegue logar (403, "Usuário inativo.", só com a senha certa) | Decisão R6 do review; `LoginUseCase` | 2026-10-27 | implementado |
| RN-AC03 | Credencial inválida devolve mensagem genérica ("E-mail ou senha inválidos."), com 401, exista ou não o e-mail | Código; TCC quadro 3 | 2026-10-11 | implementado |
| RN-AC04 | Só existe o perfil Administrador: todo usuário nasce Admin e o perfil não vem do front | Decisão global 0004 | 2026-10-27 | implementado |
| RN-AC05 | Senha guardada com hash (BCrypt); nunca devolvida pela API | TCC RNF004; `PasswordHasher` | 2026-10-30 | implementado |
| RN-AC06 | Autenticação fica em `/api/auth` (login, me, troca de senha), separada do CRUD de `/api/users` | L-AC1, recomendação adotada | 2026-10-30 | implementado |
| RN-AC07 | Não se inativa o próprio usuário nem o último Admin ativo (400) | L-AC2, recomendação adotada | 2026-10-30 | implementado |
| RN-AC08 | Senha com mínimo de 8 caracteres, ao menos uma letra e um número (máximo de 100); maiúscula e símbolo não são exigidos. Vale para criar, editar e trocar. O login não aplica a política | L-AC3, recomendação adotada | 2026-10-30 | implementado |
| RN-AC09 | Token dura 8 h, sem refresh token nem "lembrar-me" nesta versão | L-AC4, recomendação adotada | 2026-10-30 | implementado |
| RN-AC10 | Usuário inativo é checado a cada requisição autenticada (`OnTokenValidated`): perde o acesso na hora, com 401, mesmo com token válido; o front encerra a sessão em qualquer 401 | Decisão 2 de 29/10/2026 (Daniel delegou) | 2026-10-29 | implementado |
| RN-AC11 | A última loja usada fica no `localStorage` do front; `lastStoreId` sai do contrato | Decisão 1 de 29/10/2026 (Daniel delegou) | 2026-10-29 | decidido; implementado na F0.6 |
| RN-AC12 | O último acesso (`lastLoginAt`) é gravado a cada login com sucesso e aparece na listagem | L-AC5, recomendação adotada | 2026-10-30 | implementado |
| RN-AC13 | Usuário inativo não pode ser editado (400); reative antes. O CPF não muda depois de criado | `UpdateUseCaseBase`, `UpdateUserRequestDto`; decidido na F0.4 pela coerência com o contrato T-AC3 | 2026-10-30 | comportamento atual |
| RN-AC14 | A troca da própria senha exige a senha atual, e a nova precisa ser diferente dela | `ChangePasswordUseCase`, contrato T-AC4 | 2026-10-30 | comportamento atual |

## Riscos conhecidos

| Risco | Decisão | Fonte | Data | Status |
|--|--|--|--|--|
| Corrida do último Admin (RN-AC07): dois Admins inativando um ao outro no mesmo instante passam ambos pela checagem e podem deixar a empresa sem Admin ativo | Aceito pelo porte de 4 a 15 funcionários, em que a coincidência é rara, e porque o ADR 0010 não tem transação manual. A correção, se ocorrer, é reativar direto no banco | Validação da F0.4; ADR 0010 | 2026-10-30 | risco aceito |

## Perguntas em aberto
- Nenhuma neste módulo. As duas anteriores (inativar a si mesmo/último Admin; política de senha) foram fechadas por RN-AC07 e RN-AC08.
