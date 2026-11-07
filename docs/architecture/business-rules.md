# Regras de negócio transversais

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> Regras que valem para o produto inteiro. Regras de um módulo ficam em `modules/<módulo>/business-rules.md`.
> "Comportamento atual" = o código faz assim, mas ninguém decidiu que deve ser assim.

| ID | Regra | Fonte | Data | Status |
|--|--|--|--|--|
| RN-G01 | Toda rota exige login; não há área pública além do login | Decisão R2 do review | 2026-10-27 | decidido (rascunho) |
| RN-G02 | Existe só o perfil Administrador; permissões modulares ficam para o futuro | Decisão R2 do review / decisão 0004 | 2026-10-27 | decidido (rascunho) |
| RN-G03 | Datas de negócio ("hoje", mês de venda, vigência) usam o fuso `America/Sao_Paulo`; persistência em UTC | `BusinessClock` (API) | 2026-10-11 | comportamento atual |
| RN-G04 | Cadastros principais não são apagados: são inativados e podem ser reativados (soft delete) | `IDeletable`, rotas de reativação | 2026-10-11 | comportamento atual |
| RN-G05 | Valores monetários em reais (BRL); sem multimoeda | Código e TCC | 2026-10-28 | rascunho / a validar |
| RN-G06 | Nenhuma ação sugerida pela IA é executada sem confirmação humana | `AI_FORECAST_SPEC.md` §1 e §10 | 2026-10-11 | rascunho / a validar |
| RN-G07 | Documento fiscal (NF-e/NFC-e) não é emitido nem lido pelo sistema | Decisão 0002 | 2026-10-27 | decidido (rascunho) |

## Perguntas em aberto
- RN-G05: algum público-alvo precisaria de outra moeda? (provavelmente não)
- Deve existir trilha de auditoria (quem fez o quê) já na versão do TCC?
