# Contrato front × back — convenções

> **Status:** rascunho para validação · **Atualizado:** 2026-10-28 (envelope e nomes de DTO pelo ADR 0010)
> Cada módulo tem seu `contract.md` em `../modules/<módulo>/contract.md`: telas → informações carregadas → ações → endpoints → DTOs.
> As regras citadas (`RN-*`) estão no `business-rules.md` de cada módulo. Mudou um DTO aqui? Muda nos dois repositórios.

## Índice
| Módulo | Contrato |
|--|--|
| Catálogo e estoque | `../modules/catalog-inventory/contract.md` |
| Vendas | `../modules/sales/contract.md` |
| Compras e cadastros (fornecedores, clientes) | `../modules/purchasing/contract.md` |
| Inteligência de compras, painel e notificações | `../modules/demand-forecast/contract.md` |
| Acesso | `../modules/access/contract.md` |

## Envelope (padrão atrena, ADR 0010)
```ts
// sucesso: o corpo é o próprio DTO, sem envelope
PaginationDto<T>      { items: T[]; total: number }                      // toda listagem
ResultDto             { isSuccess: false; errors: string[]; fieldErrors?: Record<string, string[]>;
                        errorCode: number; message: string; data?: unknown }   // toda falha
Option                { value: string; label: string }
```
- Erros: 400 regra de negócio, 401 sem login, 404 não encontrado, 409 conflito de concorrência (saldo ou versão mudou),
  422 validação (`fieldErrors` por campo, em camelCase), 500 inesperado. Corpo que não vira DTO: campo com valor inconversível
  (data `"xx"`) é 422 no campo, com "Valor inválido."; corpo vazio ou JSON ilegível é 400 (`ApiController`, F0.4, 2026-10-30).
- **Aviso que pede confirmação** (ex.: promoção abaixo do custo, RN-VD13): a API responde 422 com `fieldErrors.confirm = ["mensagem"]`;
  o front mostra a mensagem e reenvia com `confirmWarnings: true` no corpo.
- Inativar é `DELETE /<recurso>/{id}` (soft delete); reativar é `PATCH /<recurso>/{id}/reactivate`.
- Nomes de DTO nos contratos dos módulos: onde estiver `SaveXxxDto`/`CreateXxxDto` leia `XxxRequestDto`; `UpdateXxxDto` vira
  `UpdateXxxRequestDto` só quando aceita menos campos; `XxxDetailDto` vira `XxxResponseDto`. `XxxListItemDto`, `XxxFormDto` e
  `XxxOptionDto` continuam (exceções do ADR 0010). Os contratos são renomeados quando cada módulo for implementado.
- Rotas de ativo/inativo escritas como `PATCH /{id}/active { isActive }` nos contratos seguem a regra acima.

## Listagens
- Query: `?offset=0&limit=20&filters={json}&sort=campo&order=asc|desc`. Filtros genéricos como hoje (`nextflow/docs/FILTERS.md`).
- Toda listagem devolve `PaginationDto<XxxListItemDto>`: DTO **enxuto**, só com o que a tabela mostra.
- Detalhe devolve `XxxResponseDto`; formulário envia `XxxRequestDto` (ou `UpdateXxxRequestDto`).
- Combos (SearchSelect) usam `GET /<recurso>/options?search=` → `Option[]` ou um `XxxOptionDto` quando o combo precisa de mais dados (ex.: preço).

## Tipos
- JSON em camelCase. Ids `string` (Guid). Dinheiro e quantidade `number` (decimal no banco; quantidade respeita `decimalPlaces` do produto).
- Datas: `DateOnly` → `"2026-10-28"`; instante → ISO UTC `"2026-10-28T23:40:00Z"` (o front mostra no fuso de São Paulo).
- Enums trafegam como **string** (nome em inglês, `GetApiName()` na API) e o front tem o label pt-BR em `types/enums.ts`.
- Campos calculados vêm prontos da API (preço efetivo, disponível, custo médio, status de promoção, totais). O front nunca recalcula regra.
- Toda referência a outra entidade que a tela **mostra** vem com o nome junto (`supplierId` + `supplierName`), para o front não fazer outra chamada.

## Concorrência
- Documentos editáveis (pedido, compra, transferência, inventário) trazem `version: number`; o update envia a mesma `version`.
  Se mudou, 409 com mensagem "Este registro foi alterado por outra pessoa".

## Lacunas encontradas ao escrever os contratos (28/10/2026)
Cada uma tem recomendação no contrato do módulo. Todas adotadas (as 4 que dependiam do Daniel foram decididas em 28/10/2026).
| ID | Tema | Recomendação |
|--|--|--|
| L1 | Valor de atributo novo na mesma requisição | `tempKey` |
| L2 | Inventário "cego" | opção ao abrir |
| L3 | Venda com inventário aberto | permitir; esperado ajustado |
| L4 | Motivo "Ajuste" genérico | sim, com observação obrigatória |
| L5 | Saldo de abertura com custo | entra no custo médio |
| L-VD1 | Orçamento vencido | status Expirado + ação Renovar |
| L-VD2 | Validade do orçamento | 7 dias, editável 1–30 |
| L-VD3 | Orçamento sem estoque | avisa, permite; bloqueia no pagamento |
| L-VD4 | Preço do orçamento | **decidido 28/10**: congelar durante a validade (RN-VD19) |
| L-VD5 | Promoções | mostrar unidades vendidas na promoção |
| L-VD6 | Boleto | **decidido 28/10**: removido (RN-VD20) |
| L-VD7 | Pedido pago | só sai por reembolso; cancelar só orçamento |
| L-VD8 | 7 dias do reembolso | contar de `paidAt` |
| L-VD9 | Reembolso parcial | fora do escopo |
| L-VD10 | Promoção do produto × da variação | conflitam no mesmo período |
| L-CP1 | Entrega com divergência | receber tudo + botão "receber com divergência" que abre ajuste |
| L-CP2 | Mínimo e múltiplo do fornecedor | avisar e confirmar (não bloquear) |
| L-CP3 | Lead time real | **decidido 28/10**: contar do envio ao fornecedor (`sentAt`) (RN-CP08) |
| L-CP4 | Recebimento retroativo | até 7 dias |
| L-CP5 | Cancelar compra gerada pela IA | recomendação volta a Pendente se a análise ainda é a última |
| L-CP6 | CPF do cliente | opcional, único quando informado |
| L-CP7 | Aniversário do cliente | só filtro "aniversariantes do mês" |
| L-CP8 | Número sequencial visível | sequência no banco para pedidos, compras, transferências, inventários |
| L-DF1 | Análise demorada | **decidido 28/10**: segundo plano, status Running, progresso, notificação ao fim (RN-DF23) |
| L-DF2 | Horizonte único na análise | projeta até o horizonte; necessidade usa o lead time de cada produto |
| L-DF3 | Precisão com ruptura | ignorar meses com > 50% dos dias sem estoque |
| L-DF4 | Notificação de estoque baixo/lote | resumo diário, não uma por evento |
| L-DF5 | Variação sem histórico no rateio | divisão igual, editável no dialog |
| L-DF6 | Transferir sem previsão por loja | saldo × mínimo/cobertura por local |
| L-DF7 | Expirar recomendações antigas | só quando a nova análise conclui |
| L-DF8 | Quem recebe notificação | todos os usuários ativos (todos Admin) |
| L-AC1 | Rotas de login | mover para `/api/auth` |
| L-AC2 | Inativar a si mesmo / último Admin | bloquear |
| L-AC3 | Senha | mínimo 8, letra e número |
| L-AC4 | Token | 8 h, sem refresh |
| L-AC5 | Último acesso | registrar |
