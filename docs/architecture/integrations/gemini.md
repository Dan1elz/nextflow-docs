# Integração — Google Gemini (IA da previsão)

> **Status:** rascunho / a validar · **Atualizado:** 2026-11-08 (modelo reserva)
> **Origem:** `nextflow/docs/AI_FORECAST_SPEC.md` §6 · Módulo: `modules/demand-forecast`

## Para que serve
Recebe o resultado do cálculo de previsão e devolve priorização e motivos em pt-BR. Não gera números próprios (decisão 0005).

## Contrato
| Item | Valor |
|--|--|
| Abstração | `IAiClient` (`IsConfigured`, `ProviderName`, `Model`, `GenerateJsonAsync`) |
| Implementação | `GeminiAiClient` |
| Endpoint | `POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent` |
| Autenticação | header `x-goog-api-key` (chave em `Ai:ApiKey`, nunca logada) |
| Formato | `responseMimeType=application/json` + `responseSchema`; temperatura 0.2 |
| Limites | até 40 produtos por chamada; timeout `Ai:TimeoutSeconds` (60) **por tentativa**; até 2 tentativas por modelo em 429/500/503 |
| Configuração | `Ai:Provider`, `Ai:ApiKey`, `Ai:Model` (`gemini-flash-latest`), `Ai:FallbackModel` (`gemini-flash-lite-latest`), `Ai:TimeoutSeconds` |
| Variáveis do compose | `AI_PROVIDER`, `AI_API_KEY`, `AI_MODEL`, `AI_FALLBACK_MODEL` (`.env.example`, `compose.development/staging/vm-dev.yaml`) |

## Modelo reserva (08/11/2026, back `dcd1e3b`, branch `feat/bloco-c-previsao`)
Em 08/11 o `gemini-flash-latest` passou a responder 503 "high demand" e a segurar a conexão por até 141 s; como o prazo de 60 s valia
para todas as tentativas juntas, os lotes caíam para o cálculo e a análise saía "Concluída sem IA". Desde `dcd1e3b`:
- o prazo é **por tentativa**, com até 2 tentativas por modelo em 429/500/503;
- tempo esgotado, 404 ou as tentativas esgotadas vão para `Ai:FallbackModel` (padrão `gemini-flash-lite-latest`);
- a análise grava em `aiModel` o modelo que de fato respondeu.
Medido em 08/11: só com o lite a análise inteira leva ~15 s; com o flash-latest sobrecarregado, ~3,5 min até cair no reserva.
Os modelos `gemini-2.5-*` devolvem 404 para chaves novas. Testes novos em `GeminiAiClientTests`; suíte 1003/1003.

**Dev:** `~/Projetos/nextflow/nextflow/.env` (fora do git) tem só `AI_PROVIDER`, `AI_API_KEY` e `AI_MODEL=gemini-flash-latest`;
o resto segue os padrões do compose. Confira com `GET /api/settings/forecast` (`aiConfigured`). Trocar `AI_MODEL` para o lite no dev
foi sugerido ao Daniel (aguardando).

## Falhas
Sem chave, ou principal **e** reserva com timeout, erro ou JSON inválido → recomendações 100% do cálculo, `Status = CompletedWithoutAi`, `ErrorMessage` explica.

## Guardrails aplicados à resposta
Ver `modules/demand-forecast/business-rules.md` (RN-DF10 a RN-DF14).

## Perguntas em aberto
- Custo e cota: plano gratuito do Gemini atende a demo e um uso real?
- Os dados de vendas enviados ao Google exigem aviso ao lojista (LGPD)? Hoje não vão dados pessoais de clientes.
