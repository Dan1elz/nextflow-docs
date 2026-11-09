# Ideia pós-TCC: previsão por loja

> **Status:** ideia, fora do escopo do TCC (decisão do Daniel, 08/11/2026). Na banca a previsão é da empresa inteira (ADR 0001 do
> módulo), com a compra dividida entre lojas pela falta de cada uma (RN-DF27, F3.9). Este documento guarda o desenho para depois.

## Problema
Hoje a análise projeta a demanda **por produto, na empresa inteira** (histórico mensal, sazonalidade e projeção da empresa) e só no
fim divide a compra entre as lojas pela participação nas vendas. Isso tem dois efeitos:
- A sobra de uma loja reduz a compra da outra. Ex.: loja A vende 300/mês e tem 350; loja B vende 120/mês e tem 350. Somadas, a
  empresa parece coberta, mas a loja A precisa comprar e a B não.
- A sazonalidade é uma só. Lojas com picos diferentes (shopping no Natal, centro no Dia das Mães) recebem a mesma curva.

O Daniel quer abrir o "Comprar" e já ver quanto vai para cada loja, sem dividir à mão.

## Desenho proposto
1. **Histórico por loja:** venda mensal, dias sem estoque e demanda perdida por produto × loja (tabela nova ao lado de
   `product_sales_monthly`, montada pelo mesmo job de dados derivados a partir das vendas pagas; o `orders.store_id` já é gravado).
2. **Sazonalidade por loja:** índice mensal da própria loja quando ela tem 12+ meses de histórico; abaixo disso, a curva da
   empresa aplicada ao nível de venda da loja (ou uma média ponderada entre as duas, a calibrar).
3. **Cálculo por produto × loja:** demanda projetada da loja no horizonte, saldo e "a caminho" da loja, mínimo da loja.
   Necessidade da loja = venda até a compra chegar + cobertura alvo + segurança − saldo − a caminho, nunca abaixo de zero.
4. **Recomendação continua uma por produto** (a lista não multiplica): "Comprar" = soma das necessidades das lojas, com a parte de
   cada loja gravada em `forecast_recommendation_stores` (tabela que já existe). Deixa de ser rateio e passa a ser a conta da loja.
5. **IA:** recebe, por produto, as linhas de cada loja e pode ajustar a quantidade de cada loja dentro de RN-DF12 (0,5×–1,5× do
   calculado), explicando por loja. Mesmo número de chamadas; payload maior.
6. **Comprar:** abre já com um pedido por fornecedor × loja, cada um no local de recebimento da loja; o Admin só confere e ajusta.
   O interruptor "Dividir entre lojas" e o local de entrega do grupo saem.
7. **Transferir:** continua antes de comprar quando uma loja sobra e outra falta (RN-DF16).
8. **Precisão (RN-DF19):** medir por loja também, para ver qual loja a previsão erra mais.

## O que muda na documentação
- ADR 0001 do módulo (previsão da empresa) é substituída por uma nova.
- RN-DF27 (rateio pela falta) vira "necessidade calculada por loja"; RN-DF12 passa a valer por loja.
- Migration para o histórico por loja (e, se for o caso, sazonalidade por loja).

## Esforço estimado
3 a 4 horas de desenvolvimento com testes (histórico e sazonalidade por loja, motor, IA, comprar, docs), mais a suíte completa.

## Versão intermediária (também pós-TCC, se quiser um passo menor)
Sem sazonalidade por loja: necessidade de cada loja = demanda da empresa × participação da loja − saldo − a caminho, com zero para
loja com sobra; "Comprar" = soma dessas necessidades (a sobra da loja B deixa de reduzir a compra da loja A).
