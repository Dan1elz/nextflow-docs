# Módulo Cadastros — regras de negócio

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-30
> **Origem:** código da API, documentação dos repositórios, lacunas L-CP6 e L-CP7 de `purchasing/contract.md`, decisões delegadas pelo Daniel em 29/10/2026

| ID | Regra | Fonte | Data | Status |
|--|--|--|--|--|
| RN-CD01 | CPF de cliente é opcional; quando informado é único e validado, com erro no campo (422). Vazio grava nulo | L-CP6, recomendação adotada; `CreateClientUseCase`, índice único em `clients.cpf` | 2026-10-30 | implementado |
| RN-CD02 | CNPJ de fornecedor é obrigatório, único e validado, com erro no campo (422) | `CreateSupplierUseCase`, índice único em `suppliers.cnpj` | 2026-10-30 | implementado |
| RN-CD03 | Prazo de entrega do fornecedor: 1 a 180 dias, padrão 7 | `SupplierRequestDtoValidator`, `CHECK` em `suppliers` | 2026-10-30 | implementado |
| RN-CD04 | Cliente e fornecedor são inativados, não apagados, e podem ser reativados; inativo sai dos combos e não pode ser editado (400) | `IDeletable`, `GetOptionsUseCaseBase`, `UpdateUseCaseBase` | 2026-10-30 | implementado |
| RN-CD05 | Endereço e contato pertencem a um dono (cliente ou fornecedor) por `owner_type` + `owner_id`, sem FK: `CHECK` de `owner_type` no banco e existência do dono validada no use case (404). O dono não muda na edição. Exclusão física | `DOMAIN_LEVELS.md`; decisão 4 de 29/10/2026 (Daniel delegou) | 2026-10-29 | implementado |
| RN-CD06 | No máximo um endereço e um contato principais por dono: marcar desmarca os outros no mesmo commit, e o primeiro registro do dono já nasce principal. Zero principal é aceito: desmarcar o principal ou excluí-lo não promove outro, e a listagem do dono fica sem cidade ou contato até marcar um. O telefone da listagem e do combo de cliente só vem do contato principal do tipo telefone ou WhatsApp: com zero principal ou principal e-mail fica nulo | Decisão 4 de 29/10/2026; "no máximo um" decidido pelo coordenador após os testes da F0.5 | 2026-10-30 | implementado |
| RN-CD07 | Aniversariantes: só o filtro do mês, pela data de negócio (`IBusinessClock`), sem campanhas nem observações | L-CP7, recomendação adotada | 2026-10-30 | implementado |
| RN-CD08 | País, estado e cidade são só leitura, com seed do IBGE; as telas de CRUD saíram do front | Decisão 5 de 29/10/2026 (Daniel delegou) | 2026-10-29 | implementado |
| RN-CD09 | Cadastro rápido de cliente: nome e telefone (10 ou 11 dígitos), com o telefone como contato principal no mesmo commit | `purchasing/contract.md` T-CD4 | 2026-10-30 | implementado na API; a tela entra com a venda (F2.4) |
| RN-CD10 | Dono inativo não recebe endereço nem contato: criar e editar devolvem 400, como a edição do próprio cadastro inativo. A listagem continua, e reativar o dono libera de novo | Decidido pelo coordenador após os testes da F0.5; `OwnerRules.CheckOwner` | 2026-10-30 | implementado |

## Riscos conhecidos

| Risco | Decisão | Fonte | Data | Status |
|--|--|--|--|--|
| Dono apagado direto no banco deixa endereço e contato órfãos, porque não há FK | Aceito: cliente e fornecedor só são inativados (RN-CD04), nunca apagados pela API | `DOMAIN_LEVELS.md`, inconsistência 1 | 2026-10-30 | risco aceito |
| Sem índice parcial em `is_main`, requisições simultâneas podem deixar dois principais no mesmo dono (RN-CD06) | Aceito pelo porte de 4 a 15 funcionários: a coincidência é rara e marcar de novo corrige | Validação da F0.5 | 2026-10-31 | risco aceito |
| Duplicado simultâneo de CPF ou CNPJ passa pela checagem e bate no índice único: o banco recusa, mas a resposta é 500, não 422 no campo (RN-CD01, RN-CD02) | Aceito pelo porte de 4 a 15 funcionários: o dado não corrompe e repetir o envio devolve o 422 | Validação da F0.5 | 2026-10-31 | risco aceito |

## Perguntas em aberto
- Cliente pessoa jurídica (CNPJ) é necessário?
