# Integração — ViaCEP

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** `nextflow-front/docs/PROJECT.md` (`viacep.service.ts`) e `nextflow/docs/PROJECT.md` (`AddressesController`, resolução de CEP)

## Contrato
| Item | Valor |
|--|--|
| Uso | Preencher endereço a partir do CEP no cadastro de cliente/fornecedor |
| Chamada | `viacep.com.br` (API pública, sem chave) |
| Onde | front (`viacep.service.ts`) e API (resolução de CEP em `/api/addresses`) |

## Perguntas em aberto
- Por que existem duas chamadas (front e API)? Manter só uma?
- O que acontece sem internet ou com CEP inexistente?
