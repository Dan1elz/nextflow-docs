# Nextflow — visão do produto

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** mensagem do Daniel de 28/10/2026 (público e modularização), texto do TCC v9 (cap. 1 e 4), `nextflow/docs/PROJECT.md`, `AI_FORECAST_SPEC.md`, decisões de 27/10/2026
> registradas no doc de achados do review. O produto vai mudar: este texto é ponto de partida da entrevista, não especificação.

## 1. O que é
O Nextflow é um **ERP web modular para comércios pequenos e médios**, de qualquer segmento (padaria, papelaria, loja de
roupas, atacado de tecidos etc.). O núcleo é **gestão de produtos, estoque e vendas**; o diferencial é a
**inteligência de compras**: a partir do histórico de vendas, prever a demanda (inclusive sazonal) e recomendar
**Comprar**, **Promover** ou **Manter** cada produto.

Princípio do diferencial: **o backend calcula, a IA interpreta, o humano decide.**

## 2. Problema que resolve (hipótese, a validar)
Fontes: Sebrae/CDL-BH (mapeamento Varejo Inteligente Conecta Brasil, 1.334 pequenos negócios, 2023), justificativa do TCC
(Sebrae, NIC.br), páginas de concorrentes (Omie, Bling).
- Gestão do negócio, vendas e caixa aparecem como os maiores desafios; estoque e controle de caixa sofrem com falta de
  capacitação e processos manuais.
- Estoque controlado "de olho" ou em planilha: compra no escuro, ruptura no pico e sobra parada.
- Dados desconectados: venda, estoque e dinheiro não conversam, então o dono não sabe o lucro real.
- Com 4 a 15 funcionários, várias pessoas vendem e mexem no estoque: sem perfis e registro de quem fez o quê, o controle se perde.

## 3. Para quem
- **Público (definido em 28/10/2026 pelo Daniel):** empresas pequenas e médias de **4 a 15 funcionários**, de **qualquer
  tipo de comércio**. A previsão sazonal é um módulo diferencial, não o recorte de público.
- **Consequência:** o catálogo precisa servir segmentos diferentes (grade de tamanho/cor na roupa, venda por kg na padaria,
  por metro e preço de atacado no tecido). Ver lacunas na seção 5.
- **Perfis de uso:** só **Administrador** (decisão 0004, reafirmada em 28/10/2026). Estoquista, comprador e lojista são futuro;
  o desenho de recebimento e transferência já prevê etapas com status para isso.

## 4. Escopo (atualizado em 28/10/2026 após a entrevista)
| Dentro | Fora / futuro |
|--|--|
| Catálogo com grade, tipo de produto, coleção, ciclo de vida, categoria em 2 níveis | Vínculo "produto substitui outro" |
| Estoque por variação × local × lote, transferência, inventário, perdas com motivo, custo médio | Conversão caixa → unidade (compra sempre por item) |
| Vários depósitos/lojas na mesma empresa (visão Admin) | Perfis estoquista / comprador / lojista |
| Venda de balcão no caminho feliz e pedido com orçamento (validade e reserva) | PDV completo (caixa, TEF, cupom, offline), troca, fiado e venda a prazo |
| Compras com local de entrega e lote/validade no recebimento | Recebimento parcial |
| Promoções com período | Exclusão de venda atípica da análise |
| **Sazonalidade com IA**: Comprar, Promover, Manter, **Transferir** | Previsão por loja (fica para depois; dado já é gravado) |
| Painel de indicadores | Financeiro (caixa, contas, lucro), CRM, comissões, multi-tenant, e-commerce, NF-e |

## 5. Módulos (validados em 28/10/2026)
| Módulo | Pasta | Conteúdo | Regras |
|--|--|--|--|
| Acesso | `architecture/modules/access` | Login e usuários; só Admin | RN-AC* |
| Cadastros | `architecture/modules/registry` | Clientes (opcionais na venda), fornecedores, endereços | RN-CD* |
| Catálogo e estoque | `architecture/modules/catalog-inventory` | Produto, variação, lojas, locais, lotes, livro-razão, inventário | RN-CE01 a CE34 |
| Vendas | `architecture/modules/sales` | Balcão, orçamento, pagamento, reembolso, promoções | RN-VD* |
| Compras | `architecture/modules/purchasing` | Pedido de compra, recebimento por local | RN-CP* |
| Inteligência de compras | `architecture/modules/demand-forecast` | Sazonalidade, recomendações, IA | RN-DF* (entrevista em andamento) |

Modelo de dados: `architecture/diagrams/der-consolidado.md`.

## 6. Jornada principal (como funciona hoje)
1. O Admin cadastra fornecedores (com prazo de entrega), categorias e produtos (preço, custo, estoque mínimo, validade).
2. Compras recebidas dão entrada no estoque e atualizam o último custo.
3. Vendas nascem como orçamento ou pedido, são pagas (uma ou mais formas de pagamento) e baixam o estoque.
4. O Admin gera a análise de previsão; o sistema recomenda Comprar/Promover/Manter com motivo.
5. O Admin aplica a recomendação (gera pedido de compra em orçamento ou cria promoção) ou descarta.

## 7. Glossário (rascunho)
| Termo | Significado |
|--|--|
| Orçamento | Pedido de venda ainda sem compromisso (`OrderType.Budget`); terá validade (decisão catalog-inventory/0001) |
| Venda | Pedido com pagamento registrado (`Sale` + `Payment`) |
| Preço efetivo | Preço de venda considerando a promoção vigente; calculado só no backend |
| Lead time | Prazo de entrega do fornecedor: média real dos últimos recebimentos, ou o valor cadastrado |
| Cobertura | Dias que o estoque atual dura na demanda projetada |
| Índice sazonal | Quanto um mês vende em relação à média mensal do produto |
| Estoque físico × disponível | Físico = o que está na prateleira; disponível = físico menos reservas (decisão catalog-inventory/0001) |

## 8. Objetivos da versão do TCC (a validar)
- Apresentar em **dezembro/2026** (data não fixada) um produto coerente com o texto do TCC ajustado ao novo posicionamento.
- Demonstrar a previsão com o seed de 36 meses de uma loja de doces e presentes.
- Se as melhorias não ficarem prontas, apresenta-se a versão anterior.

## Perguntas em aberto
- Qual é a dor nº 1 desse público (estoque, caixa ou vendas)?
- O que o produto precisa provar na banca e o que precisa provar para um usuário real?
- O que é sucesso daqui a 6 meses (TCC aprovado, um lojista usando, portfólio)?
