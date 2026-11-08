# Gemini (particularidades)

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** `AI_FORECAST_SPEC.md` §6

Contrato completo em `../../../integrations/gemini.md`. Particularidades que afetam o módulo:
- `responseSchema` aceita só um subconjunto do OpenAPI; a leitura da resposta é tolerante.
- Modelo `gemini-flash-latest` muda sem aviso (alias): resultados podem variar entre análises.
- Máximo de 40 produtos por chamada: candidatos a Comprar/Promover primeiro, depois maior receita.
- Sobrecarga do alias (08/11/2026): 503 "high demand" com conexão presa por minutos. Desde `dcd1e3b` o prazo é por tentativa e o lote
  cai para `Ai:FallbackModel` (`gemini-flash-lite-latest`) antes de cair para o cálculo; `aiModel` da análise registra quem respondeu.
