# Cartões de fatia — ponto de entrada da implementação

> **Status:** decidido (rascunho) · **Data:** 2026-11-01 · **Origem:** auditoria de consumo
> (https://claude.ai/artifact/PmaKXqyHBKBdEJMUETbZrz).

Uma sessão nova por fatia. Ela lê **só** isto, nesta ordem, e nada mais por padrão:

1. `rules-cheatsheet.md` (regras que a verificação cobra, ~4 KB).
2. O cartão da fatia (`F1.4.md` etc., ≤ 3 KB).
3. Os arquivos da fatia de referência indicados no cartão, para copiar a forma.
4. Trechos citados pelo cartão (por ID de regra ou seção `T*` do contrato), com `grep -n`, não o arquivo inteiro.

Os guias completos (`dotnet-development-guidelines.md`, `C_SHARP_ARCHITECTURE_RULES.md`, `DOMAIN_LEVELS.md`,
`engineering-guidelines.md` do front) são **consulta por busca**, não leitura obrigatória. `PROJECT.md`, `FILTERS.md`,
`AI_FORECAST_SPEC.md` e `diagramas.md` descrevem o código antigo: só a F3.2 abre o `AI_FORECAST_SPEC.md`.

## Esteira (decidida pelo Daniel em 01/11/2026)
| Status | Quem | O que acontece |
|--|--|--|
| `A fazer` | orquestrador | Abre uma thread de desenvolvimento com o cartão |
| `Em dev` | thread dev | Implementa contra o cartão. **Sem rodar teste, lint ou build a cada passo** |
| `Under review` | thread dev → orquestrador | Antes de subir: `dotnet format --verify-no-changes`, `dotnet build -warnaserror`, testes do módulo, `npm run lint`, `npm run build`, uma vez. Commit local e linha no quadro |
| `Under review` | thread review (nova) | Lê só cartão + diff do commit + `rules-cheatsheet.md`. Confere cada critério de aceite e cada teste listado no cartão. Só código, sem Playwright |
| `Devolvida` | review → dev | Lista objetiva do que falhou, por critério; a dev corrige e sobe de novo |
| `Aprovada` | orquestrador | Fecha as duas threads; push no fim do bloco |
| `QA Daniel` | Daniel | Teste manual no fim do bloco |

Regras da thread dev:
- Lê só `rules-cheatsheet.md`, o cartão e a fatia de referência; trechos do contrato por `grep`, nunca o arquivo inteiro.
- Os testes listados no cartão são obrigatórios e com esses nomes; caso de borda fora do cartão vira 400/422 e uma linha
  em "Em aberto". **Sem RN nova.** Sem teste de mutação.
- Modelo: Opus nas fatias "densa", Sonnet nas demais.

## Ordem (núcleo da banca)
| Bloco | Fatias | Marco |
|--|--|--|
| A | F1.3 (fechar), F1.4, F1.5 *densa*, F1.6, F1.8, F1.11 | Catálogo com saldo pelo ledger e seed do catálogo |
| B | F2.1, F2.3, F2.4 *densa*, F2.7, F2.8 *densa*, F2.9, F2.10 | Venda e compra no staging com 36 meses |
| C | F3.1, F3.2 *densa* + F3.7, F3.3, F3.4 *densa*, F3.5 | Previsão de ponta a ponta |
| Opcional | F2.2, F1.7, F2.5, F2.6, F1.9, F1.10, F3.4b, F3.6 | Só depois do bloco C |

Os cartões dos blocos B e C são escritos ao fim do bloco anterior, para refletir o código real.
