# Fonte do capítulo 6 (CONSIDERAÇÕES FINAIS). Gerado no ODT por gerar_capitulo.py, depois do cap5.py.
# Foco no produto (pedido do Daniel, 09/11): o problema do lojista e o que o sistema muda no dia a dia, não a arquitetura.

TITULO = 'CONSIDERAÇÕES FINAIS'
TITULO_SEGUINTE = 'REFERÊNCIAS'
NUMERO = '6'
FIG_INICIO = 44
QD_INICIO = 16

INTRO = ('Este trabalho partiu de um problema comum aos pequenos e médios comércios: o estoque controlado de memória ou em '
         'planilhas, compras feitas sem base em dados, falta de produtos justamente nas datas de maior venda e mercadoria '
         'parada ou vencida depois delas. O Nextflow responde a esse problema reunindo em um único sistema o cadastro de '
         'produtos, o estoque de cada loja, as vendas de balcão e as compras junto aos fornecedores, de modo que cada venda '
         'e cada recebimento atualizem o estoque no mesmo instante e fiquem registrados.')

BLOCOS = [
    ('p', 'O diferencial do produto é transformar esse histórico em decisão de compra. Em vez de o gestor estimar quanto '
          'pedir para o Natal ou para a Páscoa, o sistema indica o que comprar, em que quantidade e até quando, considerando '
          'o prazo de entrega de cada fornecedor; aponta o que promover antes que saia de época ou vença; e sugere '
          'transferir mercadoria de uma loja para outra antes de comprar mais. Cada recomendação é acompanhada do motivo e '
          'dos números que a sustentam, em linguagem simples, e a decisão final é sempre do gestor.'),
    ('p', 'Nos dados de demonstração de uma loja de doces e presentes com duas unidades e três anos de histórico, a análise '
          'antecipou a compra de produtos de Natal cujo estoque não cobriria o prazo de entrega somado ao pico de dezembro, '
          'sugeriu promoções para kits de datas já passadas com lotes próximos do vencimento e indicou transferências entre '
          'as lojas. São exatamente as situações que, sem apoio, resultariam em prateleira vazia na data comemorativa, em '
          'perda por validade ou em uma compra desnecessária.'),
    ('p', 'No dia a dia, o sistema também simplifica a operação: a venda de balcão aceita o leitor de código de barras e '
          'várias formas de pagamento, o painel mostra logo na entrada o que precisa de atenção, como estoque baixo, lotes '
          'perto do vencimento e as próximas datas comerciais, e tudo pode ser acessado pelo computador ou pelo celular, '
          'sem a necessidade de um servidor na loja. Ao oferecer esses recursos em uma ferramenta acessível, o trabalho '
          'contribui para aproximar dos pequenos negócios um tipo de gestão que, como mostram os dados apresentados na '
          'justificativa, ainda é muito mais comum nas empresas de grande porte.'),
    ('p', 'Para a equipe, o projeto proporcionou a experiência de desenvolver um produto completo, do entendimento do '
          'problema do lojista à entrega de um sistema funcional e testado, exercitando a definição de regras de negócio, a '
          'priorização do que entra em cada versão e o trabalho colaborativo.'),
    ('h2', 'Trabalhos futuros'),
    ('p', 'O próximo passo natural é colocar o Nextflow em uso em um comércio real. Além disso, destacam-se como '
          'trabalhos futuros:'),
    ('alineas', [
        ('validação em uso real', 'acompanhar a precisão da previsão ao longo dos meses com os dados de uma loja e aplicar testes de usabilidade com os usuários, por meio do questionário SUS;'),
        ('previsão por loja', 'calcular a sazonalidade e a necessidade de compra de cada unidade, e não apenas da empresa como um todo;'),
        ('perfis de acesso', 'permitir que vendedores, estoquistas e compradores usem o sistema com acesso apenas ao que precisam;'),
        ('vendas e estoque', 'pedido de venda com orçamento e reserva de estoque, reembolso de vendas e inventário por contagem;'),
        ('gestão financeira', 'fluxo de caixa, contas a pagar e a receber e indicadores de lucro;'),
        ('integração fiscal', 'entrada de mercadorias a partir do arquivo XML da nota fiscal eletrônica;'),
        ('oferta como serviço', 'permitir que vários comércios utilizem a mesma instalação, cada um com os seus dados.'),
    ]),
]
