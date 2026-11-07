# Entrevista — módulo de produto pensado para a sazonalidade

> **Status:** respondida pelo Daniel em 28/10/2026 (respostas no fim) · Objetivo: o cadastro de produto precisa guardar
> tudo o que a análise de sazonalidade (cálculo + IA) vai usar para comparar a época atual com os anos anteriores.

## A. Em que nível prever
1. Prever por variação (P azul) ou por produto (camiseta) e distribuir pela curva de grade? Recomendação: produto, distribuindo pela grade histórica.
2. Prever por loja/depósito ou só a empresa toda? Recomendação: empresa no TCC; por local depois.

## B. Histórico que atravessa os anos
3. Produto que substitui outro (novo sabor, nova embalagem) herda o histórico? Recomendação: campo "substitui o produto X".
4. Ciclo de vida: data de lançamento, "fora de linha", "só sob encomenda"? Recomendação: lançamento + status ativo / fora de linha (não recomenda compra).
5. Coleção ou temporada no produto (roupa: Verão 2026)? Recomendação: campo opcional "coleção".

## C. Sazonalidade explícita
6. Marcar eventos que puxam o produto (Páscoa, Natal, Volta às aulas, Dia das Mães)? Recomendação: tags de evento opcionais; o cálculo detecta o resto.
7. Calendário de eventos da empresa (festa local, aniversário da cidade)? Recomendação: calendário nacional fixo + eventos próprios.
8. Categoria hierárquica para produto novo herdar o padrão (Doces > Chocolates > Ovos)? Recomendação: 2 níveis.

## D. Dados que distorcem a demanda
9. Registrar demanda perdida (procurou e não tinha)? Recomendação: calcular dias sem estoque e, opcionalmente, botão "cliente procurou".
10. Venda em promoção deve ser marcada para a IA separar efeito de preço? Recomendação: sim, automático pela promoção vigente + histórico de preço.
11. Venda atípica (atacado grande) pode ser excluída da análise? Recomendação: sim, por item, com motivo.

## E. Restrições de compra
12. Por produto: fornecedor preferido, lead time do par fornecedor × produto, pedido mínimo, múltiplo da embalagem? Recomendação: sim, em produto × fornecedor.
13. Vida útil (dias) do perecível para limitar a compra ao que vende antes de vencer? Recomendação: sim, `shelf_life_days`.
14. Política por produto: cobertura alvo (dias), estoque mínimo/máximo, ou por classe ABC? Recomendação: por classe ABC, com exceção no produto.

## Respostas (Daniel, 2026-10-28)
| # | Resposta |
|--|--|
| 1 | Segue a recomendação: prever por produto e distribuir pela grade histórica |
| 2 | Segue a recomendação: empresa agora, por local depois |
| 3 | Não por enquanto: produto novo é novo registro; só flag de desativar. Vínculo "substitui X" fica para o futuro |
| 4 | Sim: flag "fora de linha" |
| 5 | A critério do Claude; precisa de trabalho de front para mostrar campos conforme o tipo de produto/segmento do cliente |
| 6 | Segue a recomendação: tags de evento opcionais |
| 7 | Segue a recomendação: calendário nacional + eventos próprios |
| 8 | Segue a recomendação: categoria em 2 níveis |
| 9 | Segue a recomendação: dias sem estoque calculados + botão "cliente procurou" |
| 10 | Segue a recomendação: venda em promoção marcada + histórico de preço |
| 11 | Fora do escopo |
| 12–14 | Sim |
