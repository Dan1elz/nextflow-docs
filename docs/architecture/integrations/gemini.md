# Integração — Google Gemini (IA da previsão)

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
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
| Limites | até 40 produtos por chamada; timeout `Ai:TimeoutSeconds` (60); até 3 tentativas em 429/500/503 |
| Configuração | `Ai:Provider`, `Ai:ApiKey`, `Ai:Model` (`gemini-flash-latest`), `Ai:TimeoutSeconds` |

## Falhas
Sem chave, timeout, erro ou JSON inválido → recomendações 100% do cálculo, `Status = CompletedWithoutAi`, `ErrorMessage` explica.

## Guardrails aplicados à resposta
Ver `modules/demand-forecast/business-rules.md` (RN-DF10 a RN-DF14).

## Perguntas em aberto
- Custo e cota: plano gratuito do Gemini atende a demo e um uso real?
- Os dados de vendas enviados ao Google exigem aviso ao lojista (LGPD)? Hoje não vão dados pessoais de clientes.
