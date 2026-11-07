# Folha de regras (o que a verificação cobra)

> Resumo de `C_SHARP_ARCHITECTURE_RULES.md` (regras inquebráveis), `dotnet-development-guidelines.md` (§20, §24, §25) e
> `nextflow-front-v2/docs/engineering-guidelines.md` (shadcn e checklist), mais os defeitos que o validador já achou nas
> F1.1–F1.3. Em dúvida, `grep` no guia completo.

## API (.NET 10)
- CRUD herda `UseCases/Base/`; um use case por operação; nunca um use case chama outro.
- Use case devolve `ResultDto<T>` via `IResultFactory<T>`; sem `throw` de negócio, sem `ActionResult`.
- Formato no FluentValidation (`Domain/Validators/`); regra de banco em `ValidateBusinessRules`; efeitos em
  `BeforePersistence`/`AfterPersistence`.
- `AppDbContext` só na Infrastructure; repositório herda `BaseRepository<T>`; commit só por `IUnitOfWork.CommitAsync()`,
  uma vez por requisição.
- Controller herda `ApiController`, usa `Handle()`, sem regra. Rotas: `DELETE` inativa, `PATCH /{id}/reactivate` reativa.
- `CancellationToken ct` em toda a cadeia; nada de `CancellationToken.None` (só em rollback), `.Result`, `.Wait()`.
- Modelo: herda `BaseModel`, sem `public set`, construtor recebe o DTO (não campos avulsos), coleções iniciadas vazias,
  navegações `virtual`.
- DTO de saída mapeia no próprio construtor; navegação de objeto único checada com `!= null`. Um DTO por arquivo.
- `Include` só no `GetInclude()` do use case.
- Estoque só pelo `IStockLedger`; movimento, pagamento e histórico de preço nunca editados nem apagados.
- Preço efetivo só pelo `IProductPricingService`; data de negócio só pelo `IBusinessClock` (nunca `DateTime.Now`).
- Enum novo também em `nextflow-front-v2/src/types/enums.ts`, com chave string.
- Teste: `Should_<resultado>_When_<condição>`, `[Trait("Rule", "RN-…")]`; unitário com mock só nas bordas; integração
  com Postgres real para ledger, venda e compra.
- Migration: `dotnet ef migrations add <Nome> --project nextflow.Infrastructure --startup-project nextflow`.

## Front (React + shadcn)
- Componente antes de markup (`Alert`, `Empty`, `Skeleton`, `Badge`, `Separator`).
- Cores semânticas; nunca cor crua nem `dark:` manual. `className` só para layout.
- `gap` em vez de `space-*`; `size-4` em vez de `h-4 w-4`.
- Formulário com `FieldGroup`/`Field`/`FieldError`, `data-invalid` e `aria-invalid`; 422 por campo no `Field` certo; 409 tratado;
  aviso de confirmação via `confirmWarnings`.
- Botão sem `isLoading`: `Button` + `Spinner` + `disabled`. Overlays com título. Itens dentro dos grupos.
- Tipos em `src/interfaces/` iguais ao `contract.md`. Service sem estado, hook sem JSX. Nada recalculado que a API devolve.
- Telas em pt-BR, responsivas até 375 px.

## Documentação
- DTO divergiu: atualize o `contract.md` do módulo. Decisão técnica: uma linha no log. RN nova só com bloqueio real.
