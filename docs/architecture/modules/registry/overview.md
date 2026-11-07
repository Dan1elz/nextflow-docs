# Módulo Cadastros — visão

> **Status:** rascunho / a validar · **Atualizado:** 2026-11-07
> **Origem:** `nextflow/docs/PROJECT.md`, `nextflow-front/docs/diagramas.md`, TCC (RF001, RF002)

## O que faz hoje
Clientes (pessoa física: nome, CPF, nascimento) e fornecedores (nome, CNPJ, prazo de entrega), cada um com endereços e
contatos. Países, estados e cidades são dados de referência, só leitura (seed IBGE, RN-CD08). CEP preenche o endereço (ViaCEP).

## API em uso (conferida no código em 07/11/2026)
O módulo não tem `contract.md` próprio; isto resume o que o código faz hoje.
- Listagens paginadas: `GET /api/clients` e `GET /api/suppliers` com `offset` (padrão 0), `limit` (padrão 20),
  `filters`, `sort`, `order`. O seletor de tamanho da página no front reflete o `limit` real (front bc58b38).
- Filtros das listagens (resolvidos antes da paginação): `stateId` e `cityId` (dono com algum endereço na UF/cidade;
  os dois juntos = interseção); `purchases` = `with`, `without`, `last30`, `last90`, `inactive90` (dias de negócio pelo
  `IBusinessClock`); no fornecedor também `pendingOrders`. Cliente compra = venda paga; fornecedor = pedido enviado ou
  recebido.
- Colunas novas: cliente `orderCount`, `totalSpent`, `lastPurchaseOn`; fornecedor `realLeadTimeDays` (média do prazo
  real dos recebidos), `productCount`, `lastPurchaseOn`.
- `GET /api/suppliers/{id}/products` (aba Produtos do fornecedor; formato no `contract.md` de purchasing). Aba Compras do
  cliente usa `GET /api/orders` filtrado por `clientId`; a do fornecedor, `GET /api/purchase-orders` por `supplierId`.
- `POST /api/clients/quick`: cadastro rápido (nome e telefone), usado na venda rápida.
- Busca de cidade (`GET /api/cities/options?search`): compara pela coluna `search_name` (só letras e dígitos, sem acento
  nem caixa; migration `AddCitySearchName`). O `LocationsSeeder` corrigiu 10 nomes do IBGE que vinham colados
  (ex.: "Santa Bárbara d'Oeste") também em bancos já carregados.
- Seed demo (`DemoRegistrySeeder`, só com `Seed:Demo:Enabled`): 12 clientes com telefone e endereço; endereço dos 5
  fornecedores; 20% das vendas do histórico com cliente.

## Perguntas em aberto
- Cliente pessoa jurídica (CNPJ) é necessário?
