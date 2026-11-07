# 0010 — API no padrão de arquitetura do atrena-api

> **Status:** decidido (rascunho)
> **Data:** 2026-10-28 · **Quem decidiu:** Daniel · **Origem:** thread "Arquitetura" do projeto; proposta
> "Nextflow — nova arquitetura (padrão atrena + shadcn)"

## Contexto
A API já usava bases de use case da mesma família do `atrena-api`, numa versão anterior: erro de negócio por exceção,
validação por DataAnnotations, `SaveChanges` em cada método do repositório e controllers montando DTO à mão. O DER
consolidado (ADRs 0007, 0008, 0009) obriga a reescrever quase todo o domínio. Alternativas: reformular no lugar (converter
o padrão e depois reescrever para o DER), esqueleto novo portando o que é compatível, ou recomeçar tudo.

## Decisão
A API é refeita sobre um esqueleto novo em .NET 10 com o núcleo do `atrena-api` (`ResultDto` + `IResultFactory`, bases de
use case com template methods, FluentValidation, commit único pelo `IUnitOfWork`, `ApiController.Handle()`,
`GlobalResultMiddleware`, Scrutor, Serilog, xUnit). Motor de previsão, storage S3, filtros, calendário comercial e lógica do
seed são portados. Os módulos são reescritos na ordem fundação → catálogo e estoque → vendas e compras → previsão, já no
DER consolidado, com uma migration inicial limpa. O front é refatorado no lugar, seguindo a skill do shadcn.

Extensões e exceções ao padrão do atrena, válidas só para o Nextflow:
1. `ResultDto` ganha `FieldErrors` (erros por campo do FluentValidation e o aviso `confirm` de RN-VD13).
2. Além de `XRequestDto`/`XResponseDto`, são permitidos `XListItemDto`, `XFormDto` (com as opções em `XFormOptionsDto`, como `ProductFormOptionsDto`) e `XOptionDto` (contratos de tela).
3. `GetAllUseCaseBase` aceita `sort`/`order` limitados a uma lista branca por use case.
4. `IStockLedger` é o único serviço que grava estoque (ADR 0007) e não faz commit.

## Consequências
- Regras de código em `nextflow/docs/C_SHARP_ARCHITECTURE_RULES.md`, `dotnet-development-guidelines.md` e
  `DOMAIN_LEVELS.md`; front em `nextflow-front/docs/engineering-guidelines.md`.
- Contrato front × back muda no transporte, não no conteúdo: sucesso sem envelope, listagem `{ items, total }`, erro
  `ResultDto`, enums como string, inativar por `DELETE` e reativar por `PATCH /reactivate` (`contracts/README.md`).
- Venda, movimento e saldo no mesmo commit, sem transação manual.
- Código da branch `task-17` vira referência de regra até cada módulo ser reescrito; o staging só troca de versão com
  vendas funcionando.
- Custo: cerca de 6 semanas de trabalho até a banca, com 1 de folga.

## Perguntas em aberto
- Data exata da banca e escopo mínimo (transferência, inventário e acerto medido podem ficar para depois).
- Divisão de trabalho entre Daniel, Ricardo e Henrique.
- Lado da FK entre recomendação e documento aplicado (`DOMAIN_LEVELS.md`, ponto 2).
