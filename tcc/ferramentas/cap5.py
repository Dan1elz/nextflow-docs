# Fonte do capítulo 5 (RESULTADOS E DISCUSSÃO). Gerado no ODT por gerar_capitulo.py, depois do cap4.py.
# Números medidos em 09/11/2026 (ver tcc/roteiro.md): suíte do back, testes do front e desempenho.

TITULO = 'RESULTADOS E DISCUSSÃO'
TITULO_SEGUINTE = 'CONSIDERAÇÕES FINAIS'
NUMERO = '5'
FIG_INICIO = 44   # o cap. 4 termina na Figura 44
QD_INICIO = 13    # e no Quadro 13

# --- números medidos (preencher a partir das execuções) ---
TESTES_BACK = '1.059 casos de teste (614 de unidade e 445 de integração)'
TEMPO_BACK = 'cerca de 11 minutos'
TESTES_FRONT = '84'

INTRO = ('Este capítulo apresenta os resultados obtidos com o desenvolvimento do Nextflow, a verificação do sistema por '
         'meio de testes automatizados e de medições de desempenho, a avaliação da interface segundo heurísticas de '
         'usabilidade e a discussão desses resultados à luz dos objetivos propostos.')

BLOCOS = [
    ('h2', 'Resultados obtidos'),
    ('p', 'O resultado do trabalho é um sistema web funcional que cobre os seis módulos descritos no capítulo anterior, '
          'com 52 casos de uso, 48 tabelas no banco de dados, uma API REST e uma interface responsiva com temas claro e '
          'escuro. A aplicação, o banco de dados e o armazenamento de objetos são executados em contêineres Docker, tanto '
          'no ambiente de desenvolvimento quanto no de homologação, hospedado em um servidor virtual.'),
    ('p', 'Para demonstrar o sistema e, em especial, a previsão, que depende de histórico, foi criado um conjunto de dados '
          'de demonstração: uma loja de doces e presentes com duas unidades, cada uma com área de venda e depósito, 42 '
          'produtos, parte deles com variações e controle de lote, 5 fornecedores e 12 clientes. O histórico de 36 meses '
          'de vendas e compras é gerado pelos mesmos serviços usados na operação, inclusive o livro-razão de estoque, com a '
          'sazonalidade de datas como Páscoa, Dia das Mães e Natal, e soma cerca de 68 mil movimentações de estoque e 21 mil vendas.'),
    ('p', 'Sobre esse histórico, a análise de previsão executada em 8 de novembro de 2026 avaliou os 42 produtos em cerca '
          'de um minuto, já incluída a revisão pela inteligência artificial, com horizonte de quatro meses, de dezembro a '
          'março. O resultado foi de 6 recomendações de compra, 2 de promoção, 4 de transferência entre lojas e 30 de '
          'manutenção do estoque (Figura 43). As compras de maior prioridade concentraram-se em produtos de Natal, como o '
          'panetone e a trufa artesanal, cuja cobertura de estoque era inferior ao prazo de entrega somado ao pico de '
          'dezembro; as promoções foram sugeridas para kits de datas já passadas com lotes próximos do vencimento, e as '
          'transferências para produtos com excesso no depósito de uma loja e falta na outra. O comportamento corresponde '
          'ao esperado pelas regras de cálculo descritas na seção 4.9.'),

    ('h2', 'Verificação do sistema'),
    ('p', 'A verificação concentrou-se em três frentes que podem ser reproduzidas pela própria equipe, sem depender da '
          'participação de usuários externos: testes automatizados, medição do tempo de resposta e avaliação heurística '
          'da interface.'),
    ('h3', 'Testes automatizados'),
    ('p', 'O *backend* possui testes de unidade, que verificam as regras isoladas, como o cálculo da previsão, a medição da '
          'precisão e os limites aplicados à resposta da inteligência artificial, e testes de integração, que exercitam a '
          'API completa contra um banco PostgreSQL real, criado em contêiner a cada execução por meio da biblioteca '
          'Testcontainers. Os testes de integração conferem as respostas da API, o que foi gravado no banco e o '
          'comportamento das transações, inclusive em gravações concorrentes. Na execução de 9 de novembro de 2026, a suíte '
          'do *backend* executou ' + TESTES_BACK + ', todos aprovados, em ' + TEMPO_BACK + '. O *frontend* '
          'possui outros ' + TESTES_FRONT + ' testes automatizados dos componentes de maior risco, como o seletor de itens '
          'da venda, a leitura de código de barras e os diálogos de aplicação das recomendações.'),
    ('p', 'O {qd:cenarios} relaciona os cenários funcionais mais relevantes, cada um coberto por pelo menos um teste '
          'automatizado, com o resultado esperado e o obtido.'),
    ('quadro', 'cenarios', 'Cenários verificados por testes automatizados.', [0.4, 2.1, 2.8, 1.0], [
        ['H:Nº', 'H:Cenário', 'H:Resultado esperado', 'H:Resultado obtido'],
        ['1', 'Autenticação com credenciais válidas', 'Token JWT emitido e último acesso registrado', 'Aprovado'],
        ['2', 'Autenticação com credenciais inválidas', 'Mesma mensagem genérica para e-mail inexistente ou senha incorreta', 'Aprovado'],
        ['3', 'Autenticação de usuário inativo', 'Acesso negado, sem registrar o acesso', 'Aprovado'],
        ['4', 'Acesso a rota protegida sem token', 'Requisição rejeitada (não autorizado)', 'Aprovado'],
        ['5', 'Venda rápida válida', 'Venda paga gravada e movimentações de saída lançadas no livro-razão', 'Aprovado'],
        ['6', 'Preço alterado desde a busca', 'Pedido de confirmação antes de gravar a venda', 'Aprovado'],
        ['7', 'Saída que deixaria o estoque negativo', 'Operação recusada quando o produto não permite negativo', 'Aprovado'],
        ['8', 'Saída sem lote escolhido', 'Baixa a partir do lote que vence primeiro', 'Aprovado'],
        ['9', 'Sequência de muitas movimentações', 'Saldo igual à soma das movimentações', 'Aprovado'],
        ['10', 'Atualização concorrente do mesmo saldo', 'Conflito detectado e segunda gravação recusada', 'Aprovado'],
        ['11', 'Recebimento de compra com custo', 'Custo médio da variação recalculado', 'Aprovado'],
        ['12', 'Transferência de item com lote', 'Entrada no destino com os mesmos lotes da saída', 'Aprovado'],
        ['13', 'Promoção abaixo do custo médio', 'Pedido de confirmação', 'Aprovado'],
        ['14', 'Segunda análise com outra em andamento', 'Nova análise recusada', 'Aprovado'],
        ['15', 'Análise sem IA configurada', 'Análise concluída apenas com o cálculo', 'Aprovado'],
        ['16', 'Quantidade da IA fora dos limites', 'Quantidade ajustada para 0,5 a 1,5 vez a calculada', 'Aprovado'],
        ['17', 'Aplicar Comprar', 'Pedido de compra em orçamento por fornecedor, ligado à recomendação', 'Aprovado'],
        ['18', 'Cancelamento de todos os pedidos de uma recomendação', 'Recomendação de volta a pendente', 'Aprovado'],
        ['19', 'Medição da precisão', 'Produto dentro da tolerância com MAPE de até 15%', 'Aprovado'],
    ]),
    ('h3', 'Desempenho'),
    ('p', 'Para verificar o RNF003, que limita a 2 segundos o tempo de resposta das consultas, as principais rotas da API '
          'foram medidas em 9 de novembro de 2026, com um banco recém-criado com os dados de demonstração (42 produtos, 36 '
          'meses de histórico, 67.809 movimentações de estoque e 20.838 vendas). A API e o banco foram executados no mesmo '
          'computador, com processador AMD Ryzen 7 5700X de 8 núcleos e 16 GB de memória. Cada consulta foi executada 20 '
          'vezes, depois de uma execução de aquecimento, medindo-se o tempo total da requisição HTTP. O {qd:desempenho} '
          'reúne os resultados.'),
    ('quadro', 'desempenho', 'Tempo de resposta das consultas.', [2.6, 0.9, 0.95, 0.95, 0.9], [
        ['H:Consulta', 'H:Execuções', 'H:Tempo médio (ms)', 'H:Maior tempo (ms)', 'H:Atende ao RNF003'],
        ['Listagem de produtos (20 por página)', '20', '16', '35', 'Sim'],
        ['Movimentações de estoque (20 por página)', '20', '44', '66', 'Sim'],
        ['Histórico de vendas (20 por página)', '20', '18', '23', 'Sim'],
        ['Painel: indicadores de vendas do mês', '20', '13', '17', 'Sim'],
        ['Painel: faturamento dos últimos 12 meses', '20', '86', '161', 'Sim'],
        ['Painel: estoque baixo', '20', '19', '25', 'Sim'],
        ['Última análise de previsão (42 recomendações)', '20', '4', '6', 'Sim'],
    ]),
    ('p', 'Todas as consultas ficaram muito abaixo do limite: a mais lenta, o gráfico de faturamento, que agrega um ano de '
          'vendas, respondeu em média em 86 milissegundos. A análise de previsão, que não é uma consulta e roda em segundo '
          'plano, levou 17 segundos para os 42 produtos quando executada apenas com o cálculo; com a revisão pela '
          'inteligência artificial, a análise de 8 de novembro levou cerca de um minuto, tempo dominado pela espera das '
          'respostas do serviço externo. Como a análise não bloqueia o uso do sistema, esse tempo não afeta as demais '
          'operações.'),
    ('h3', 'Avaliação heurística da interface'),
    ('p', 'A interface foi inspecionada pela equipe segundo as dez heurísticas de usabilidade de Nielsen (1994), que '
          'funcionam como critérios gerais de inspeção e não exigem a participação de usuários. O {qd:heuristicas} '
          'resume como cada heurística é atendida.'),
    ('quadro', 'heuristicas', 'Avaliação heurística da interface.', [2.0, 4.3], [
        ['H:Heurística', 'H:Como a interface atende'],
        ['Visibilidade do estado do sistema', 'Etiquetas de situação em vendas, pedidos e recomendações; andamento da análise atualizado na tela; sino com notificações; loja de trabalho sempre visível no topo.'],
        ['Correspondência com o mundo real', 'Termos do comércio em português (loja, local, lote, validade, pedido de compra) e caminho "Loja › Local" nas telas de estoque.'],
        ['Controle e liberdade do usuário', 'Ações de cancelar, voltar e descartar; nenhuma recomendação é aplicada sem confirmação; promoções agendadas podem ser editadas.'],
        ['Consistência e padrões', 'Mesmos componentes e o mesmo arranjo de listagem, filtros e visualização em todos os módulos.'],
        ['Prevenção de erros', 'Confirmação quando o preço muda ou a promoção fica abaixo do custo; bloqueio de estoque negativo; campos obrigatórios validados antes de gravar.'],
        ['Reconhecimento em vez de memorização', 'Busca de itens com foto, SKU e disponível; trilha de navegação no topo; sugestões já preenchidas pela análise.'],
        ['Flexibilidade e eficiência de uso', 'Leitor de código de barras na venda rápida, inclusive fora do campo de busca; filtros e ações em lote na previsão.'],
        ['Estética e design minimalista', 'Telas com poucas cores, hierarquia tipográfica clara e informações secundárias em abas e painéis laterais.'],
        ['Ajuda no reconhecimento e recuperação de erros', 'Mensagens de erro junto ao campo ou à linha do item que falhou, em português.'],
        ['Ajuda e documentação', 'Textos explicativos nas telas e, em cada recomendação, o motivo calculado e o motivo escrito pela IA.'],
    ]),

    ('h2', 'Discussão sobre os resultados'),
    ('p', 'Os resultados indicam que os objetivos propostos foram alcançados. A arquitetura em camadas e a separação em '
          'módulos permitiram que cada funcionalidade fosse construída e testada de forma independente, e a decisão de '
          'tratar o estoque como livro-razão garantiu que o saldo seja sempre explicável pelas movimentações, como exige o '
          'requisito de integridade. O módulo de previsão de demanda, diferencial do '
          'sistema, foi implementado e produz recomendações coerentes com a sazonalidade dos dados de demonstração.'),
    ('p', 'A divisão de papéis entre o cálculo e a inteligência artificial mostrou-se adequada: o modelo generativo '
          'contribui com a priorização e com explicações em linguagem natural, enquanto os números permanecem '
          'verificáveis e o sistema segue operando quando o serviço externo falha ou fica sobrecarregado, situação '
          'observada durante o desenvolvimento e tratada com um modelo reserva e com a conclusão apenas pelo cálculo.'),
    ('p', 'Algumas limitações devem ser consideradas. Os dados de demonstração são simulados e, por terem sido gerados de '
          'uma só vez, ainda não possuem análises anteriores a cada mês; por isso, a medição da precisão da previsão só '
          'produzirá resultados com o uso do sistema ao longo dos meses. A avaliação de usabilidade foi feita por inspeção '
          'heurística da própria equipe, sem testes com usuários. Por fim, esta versão possui um único perfil de acesso e '
          'a previsão é calculada para a empresa como um todo, ainda que mostre o estoque de cada loja.'),
]
