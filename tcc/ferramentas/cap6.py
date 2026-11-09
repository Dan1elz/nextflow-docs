# Fonte do capítulo 6 (CONSIDERAÇÕES FINAIS). Gerado no ODT por gerar_capitulo.py, depois do cap5.py.

TITULO = 'CONSIDERAÇÕES FINAIS'
TITULO_SEGUINTE = 'REFERÊNCIAS'
NUMERO = '6'
FIG_INICIO = 44
QD_INICIO = 16

INTRO = ('O projeto Nextflow alcançou o seu objetivo ao entregar um sistema web modular de gestão para comércios de '
         'pequeno e médio porte, que integra catálogo de produtos, estoque, vendas de balcão e compras a um módulo de '
         'previsão de demanda sazonal com apoio de inteligência artificial. A aplicação foi construída segundo os '
         'princípios da *Clean Architecture*, com as regras de negócio isoladas da infraestrutura, e a *stack* escolhida '
         '(.NET 10, React com TypeScript e PostgreSQL, executados em contêineres Docker) mostrou-se adequada: as consultas '
         'responderam, em média, em menos de 100 milissegundos com três anos de histórico, e os 1.059 testes automatizados do '
         '*backend* comprovam o comportamento das regras de negócio.')

BLOCOS = [
    ('p', 'Duas decisões se destacam como contribuições do trabalho. A primeira é tratar o estoque como um livro-razão, em '
          'que o saldo é sempre a soma de movimentações que não podem ser alteradas, o que torna cada quantidade '
          'explicável e auditável. A segunda é a divisão de papéis na previsão de demanda: o servidor calcula, a '
          'inteligência artificial prioriza e explica dentro de limites, e o gestor decide. Com isso, o sistema aproveita a '
          'capacidade dos modelos generativos de produzir explicações em linguagem natural sem depender deles para os '
          'números, e continua funcionando quando o serviço externo está indisponível.'),
    ('p', 'Do ponto de vista acadêmico, o desenvolvimento permitiu vivenciar o ciclo completo de um sistema, do '
          'levantamento de requisitos à modelagem, à implementação, aos testes e à documentação. O registro das regras de '
          'negócio com códigos, das decisões de arquitetura e dos contratos de tela, a entrega em fatias verticais e o uso '
          'de testes automatizados fortaleceram competências essenciais ao mercado, como o trabalho colaborativo, o '
          'controle de versões e a rastreabilidade entre requisito e código.'),
    ('h2', 'Trabalhos futuros'),
    ('p', 'Embora o Nextflow tenha atingido os objetivos propostos para esta versão, o projeto possui potencial de '
          'expansão. Como trabalhos futuros, destacam-se:'),
    ('alineas', [
        ('perfis de acesso', 'inclusão de perfis com permissões por módulo, como vendedor, estoquista e comprador, aplicando o princípio do menor privilégio;'),
        ('previsão por loja', 'cálculo da sazonalidade e da necessidade de compra de cada unidade, e não apenas da empresa como um todo;'),
        ('avaliação em uso real', 'acompanhamento da precisão da previsão ao longo dos meses com dados de um comércio real e testes de usabilidade com usuários, por meio do questionário SUS;'),
        ('vendas e estoque', 'pedido de venda com orçamento e reserva de estoque, reembolso de vendas e inventário por contagem;'),
        ('gestão financeira', 'fluxo de caixa, contas a pagar e a receber e indicadores de lucro;'),
        ('integração fiscal', 'entrada de mercadorias a partir do arquivo XML da nota fiscal eletrônica;'),
        ('oferta como serviço', 'separação dos dados por empresa, permitindo que vários comércios utilizem a mesma instalação.'),
    ]),
]
