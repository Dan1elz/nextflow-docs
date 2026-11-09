# Fonte do capítulo 4 (DESENVOLVIMENTO). Gerado no ODT por gerar_capitulo.py.
# Blocos: ('h2'|'h3', texto) · ('p', texto) · ('alineas', [(rotulo, texto), ...]) ·
#         ('fig', chave, legenda, caminho, largura_max_pol) · ('quadro', chave, legenda, larguras, linhas) ·
#         ('dd', chave, tabela, descricoes)  (dicionário de dados gerado do esquema)
# Marcação: *itálico*, **negrito**; {fig:chave} e {qd:chave} viram o número da figura/quadro.
# Linhas de quadro: lista de células; célula 'H:texto' = cabeçalho; '|span|' não usado.

D = '../../docs/architecture/diagrams/uml/'
S = '../../docs/screenshots/'

INTRO = ('Este capítulo apresenta o sistema Nextflow desenvolvido: a visão geral e os módulos, os requisitos e as regras de '
         'negócio, os casos de uso, a arquitetura, o modelo de domínio, o modelo de dados, os diagramas de sequência, o '
         'módulo de previsão de demanda e as interfaces de usuário.')

UC_FIGS = [
    ('uc1', 'Acesso e segurança', 'uc-1-acesso'),
    ('uc2', 'Cadastros de pessoas', 'uc-2-cadastros'),
    ('uc3', 'Catálogo de produtos', 'uc-3-catalogo'),
    ('uc4', 'Estoque', 'uc-4-estoque'),
    ('uc5', 'Vendas e promoções', 'uc-5-vendas'),
    ('uc6', 'Compras', 'uc-6-compras'),
    ('uc7', 'Previsão de demanda com IA', 'uc-7-previsao'),
    ('uc8', 'Painel e notificações', 'uc-8-painel'),
]

BLOCOS = [
    ('h2', 'Visão geral do sistema'),
    ('p', 'O Nextflow é um sistema web de gestão voltado a comércios de pequeno e médio porte, de qualquer segmento, que '
          'reúne em uma única base o catálogo de produtos, o estoque, as vendas de balcão e as compras junto aos fornecedores. '
          'Sobre esses dados opera o seu diferencial, a inteligência de compras: a partir do histórico de vendas, o sistema '
          'projeta a demanda de cada produto, inclusive a sazonal, e recomenda comprar, promover, transferir entre locais ou '
          'manter o estoque.'),
    ('p', 'O princípio que orienta esse módulo é a divisão de papéis entre o servidor, a inteligência artificial e o gestor: '
          'todos os números da previsão são produzidos por cálculo determinístico no *backend*; a inteligência artificial '
          'apenas prioriza e explica as recomendações, dentro de limites definidos; e nenhuma ação é executada sem a decisão '
          'do gestor. Assim, cada sugestão pode ser conferida e reproduzida, e o sistema continua funcionando mesmo sem o '
          'serviço de inteligência artificial.'),
    ('p', 'Nesta versão, o sistema possui um único perfil de acesso, o de Administrador, e atende uma empresa com uma ou '
          'mais lojas, cada uma com seus locais de estoque. A loja selecionada no topo da tela filtra o painel, as listagens '
          'e as operações de estoque.'),

    ('h2', 'Módulos e funcionalidades'),
    ('p', 'As funcionalidades do Nextflow estão organizadas em seis módulos:'),
    ('alineas', [
        ('acesso', 'autenticação por e-mail e senha, gestão de usuários e do próprio perfil, seleção da loja de trabalho e notificações do sistema;'),
        ('cadastros', 'clientes e fornecedores, com endereços padronizados por país, estado e cidade e preenchidos a partir do CEP, contatos por telefone, e-mail ou WhatsApp e cadastro rápido de cliente durante a venda;'),
        ('catálogo e estoque', 'produtos com tipo (padrão, vestuário, perecível ou granel), variações de grade com SKU e código de barras, categorias em dois níveis, coleções, calendário de datas comerciais, fornecedores vinculados e histórico de preço; lojas e locais de estoque; saldo por variação, local e lote, com validade; ajustes, perdas, transferências entre locais e consulta das movimentações;'),
        ('vendas', 'venda de balcão já paga, com busca por nome, SKU ou leitor de código de barras, uma ou mais formas de pagamento e troco; histórico de vendas e promoções por período;'),
        ('compras', 'pedido de compra elaborado em orçamento, enviado ao fornecedor e recebido no local de recebimento da loja, com lote e validade, atualização do custo médio e registro do prazo real de entrega;'),
        ('inteligência de compras', 'análise de previsão de demanda manual ou semanal, recomendações com prioridade, confiança e motivo, aplicação das recomendações em pedidos de compra, promoções e transferências, medição da precisão da previsão e painel com indicadores e alertas.'),
    ]),

    ('h2', 'Requisitos'),
    ('p', 'Os requisitos foram organizados em funcionais, que descrevem o que o sistema faz, e não funcionais, que estabelecem '
          'as qualidades exigidas da solução. As regras de negócio que detalham cada requisito receberam códigos por módulo.'),
    ('h3', 'Requisitos funcionais (RF)'),
    ('quadro', 'rf', 'Requisitos funcionais.', [1.0, 4.2, 1.1], [
        ['H:Identificação', 'H:Requisito funcional', 'H:Prioridade'],
        ['RF001', '**Autenticação e usuários:** autenticar o usuário por e-mail e senha, com token JWT, e permitir cadastrar, editar, ativar e desativar usuários.', 'Essencial'],
        ['RF002', '**Cadastros de pessoas:** manter clientes e fornecedores com endereços (países, estados e cidades) e contatos, com cadastro rápido de cliente na venda.', 'Essencial'],
        ['RF003', '**Catálogo de produtos:** manter produtos com tipo, variações de grade, SKU, código de barras, categorias, coleções, eventos comerciais, fornecedores, foto e histórico de preço.', 'Essencial'],
        ['RF004', '**Lojas e locais:** cadastrar lojas e seus locais de estoque, definindo os locais padrão de venda e de recebimento.', 'Essencial'],
        ['RF005', '**Controle de estoque:** manter o saldo por variação, local e lote, registrar ajustes, perdas e transferências, consultar as movimentações e definir mínimos por local e política de cobertura por classe ABC.', 'Essencial'],
        ['RF006', '**Venda de balcão:** registrar a venda paga com uma ou mais formas de pagamento, baixando o estoque do local de venda, e consultar o histórico de vendas.', 'Essencial'],
        ['RF007', '**Promoções:** cadastrar desconto por período para o produto ou uma variação, exigindo confirmação quando o preço ficar abaixo do custo médio.', 'Importante'],
        ['RF008', '**Pedidos de compra:** elaborar, enviar, receber e cancelar pedidos de compra, atualizando o estoque, o custo médio e o prazo real de entrega.', 'Essencial'],
        ['RF009', '**Previsão de demanda:** gerar a análise de forma manual ou agendada e recomendar Comprar, Promover, Transferir ou Manter para cada produto, com priorização e explicação por inteligência artificial.', 'Essencial'],
        ['RF010', '**Aplicação das recomendações:** transformar recomendações em pedidos de compra, divididos por loja, em promoções ou em transferências, ou descartá-las com motivo.', 'Essencial'],
        ['RF011', '**Precisão da previsão:** comparar a demanda projetada com a vendida em cada mês, por produto, classe ABC e categoria.', 'Importante'],
        ['RF012', '**Painel e notificações:** exibir indicadores de vendas e margem, as principais recomendações, o estoque baixo, os lotes a vencer e as próximas datas comerciais, e notificar a conclusão das análises.', 'Importante'],
    ]),
    ('h3', 'Requisitos não funcionais (RNF)'),
    ('quadro', 'rnf', 'Requisitos não funcionais.', [0.9, 3.4, 1.1, 0.9], [
        ['H:Identificação', 'H:Requisito não funcional', 'H:Categoria', 'H:Prioridade'],
        ['RNF001', '**Interface responsiva e acessível:** interface construída com componentes acessíveis (*shadcn/ui*), legível em computador e celular, com temas claro e escuro e contraste adequado (WCAG).', 'Usabilidade', 'Essencial'],
        ['RNF002', '**Integridade do estoque:** o saldo deve ser sempre igual à soma das movimentações, que não podem ser editadas nem apagadas; venda, recebimento e transferência são gravados em uma única transação, com controle de concorrência.', 'Confiabilidade', 'Essencial'],
        ['RNF003', '**Tempo de resposta:** consultas e filtros devem responder em menos de 2 segundos em condições normais de uso; a análise de previsão roda em segundo plano, sem bloquear o uso do sistema.', 'Desempenho', 'Essencial'],
        ['RNF004', '**Segurança:** senhas armazenadas com *hash*, autenticação JWT em todas as rotas da API e chaves de serviços externos fora do código-fonte.', 'Segurança', 'Essencial'],
        ['RNF005', '**Conteinerização:** a aplicação e suas dependências (banco de dados e armazenamento de objetos) devem ser empacotadas com Docker.', 'Distribuição', 'Essencial'],
        ['RNF006', '**Clean Architecture:** o *backend* deve ser organizado em camadas independentes, com as regras de negócio isoladas da infraestrutura.', 'Padrões', 'Essencial'],
        ['RNF007', '**Stack tecnológica:** React com TypeScript no *frontend*, .NET 10 (C#) com Entity Framework Core no *backend* e PostgreSQL como banco de dados.', 'Hardware/Software', 'Essencial'],
        ['RNF008', '**Funcionamento sem IA:** na falta ou falha do serviço de inteligência artificial, a análise deve ser concluída apenas com o cálculo.', 'Disponibilidade', 'Essencial'],
        ['RNF009', '**Testes automatizados:** as regras de negócio devem ser cobertas por testes automatizados de unidade e de integração.', 'Manutenibilidade', 'Importante'],
    ]),
    ('h3', 'Regras de negócio'),
    ('p', 'As regras de negócio foram registradas com um código formado pelo prefixo do módulo (AC acesso, CE catálogo e '
          'estoque, VD vendas, CP compras e DF previsão de demanda) e um número. O {qd:rn} reúne as principais, citadas nos '
          'casos de uso e nos diagramas de sequência deste capítulo.'),
    ('quadro', 'rn', 'Principais regras de negócio.', [1.0, 5.3], [
        ['H:Código', 'H:Regra'],
        ['RN-AC02', 'Usuário inativo não consegue entrar no sistema.'],
        ['RN-AC03', 'Credencial inválida recebe a mesma mensagem genérica, exista ou não o e-mail informado.'],
        ['RN-CE01', 'O saldo é a soma das movimentações; toda alteração de saldo gera uma movimentação.'],
        ['RN-CE14', 'Somente o livro-razão de estoque grava saldos e movimentações; movimentação nunca é editada nem apagada.'],
        ['RN-CE15', 'Saída sem lote escolhido é feita a partir do lote que vence primeiro (FEFO).'],
        ['RN-CE31', 'O custo médio é ponderado por variação e recalculado a cada recebimento de compra.'],
        ['RN-CE32', 'Estoque negativo é bloqueado, exceto em produto marcado como "permite negativo".'],
        ['RN-VD05', 'A soma dos pagamentos deve fechar o total da venda.'],
        ['RN-VD13', 'Promoção que deixa o preço abaixo do custo médio exige confirmação.'],
        ['RN-CP04', 'Não existe recebimento parcial: o pedido de compra é recebido por inteiro.'],
        ['RN-DF12', 'O ajuste da IA é limitado: quantidade entre 0,5 e 1,5 vez a calculada, desconto até o máximo permitido pela margem e promoção de 7 a 45 dias.'],
        ['RN-DF13', 'Se a IA falhar ou não estiver configurada, a análise é concluída apenas com o cálculo.'],
        ['RN-DF14', 'Uma nova análise expira as recomendações pendentes da análise anterior.'],
        ['RN-DF15', 'Aplicar Comprar gera pedidos de compra em orçamento; nada é enviado ao fornecedor automaticamente.'],
        ['RN-DF16', 'Recomenda-se transferir quando um local está abaixo do mínimo e outro tem excesso da mesma variação.'],
        ['RN-DF20', 'A IA recebe lotes sequenciais de até 40 produtos; um lote com falha fica com o resultado do cálculo.'],
        ['RN-DF23', 'A análise roda em segundo plano, uma por vez, e gera uma notificação ao terminar.'],
        ['RN-DF27', 'A compra pode ser dividida entre as lojas de acordo com a falta de cada uma.'],
        ['RN-DF28', 'Uma recomendação aplicada volta a pendente somente quando todos os pedidos gerados por ela forem cancelados.'],
        ['RN-DF30', 'A sugestão de compra ou de desconto pode ser pedida na hora, a partir do painel, para qualquer item em alerta.'],
    ]),

    ('h2', 'Casos de uso'),
    ('p', 'Os casos de uso descrevem as interações entre os atores e o sistema. O ator humano é o Administrador, único perfil '
          'desta versão. Há ainda dois atores de sistema: o Agendador, que dispara a análise semanal e o resumo diário de '
          'alertas, e o Serviço de IA, consultado pela análise de previsão. Todos os casos de uso, exceto o UC01, exigem '
          'autenticação.'),
    ('h3', 'Diagramas de casos de uso'),
    ('p', 'Os 52 casos de uso (UC01 a UC52) foram distribuídos em uma figura por módulo, da {fig:uc1} à {fig:uc8}, para que '
          'cada diagrama caiba em uma página. A relação *include* indica um passo que sempre ocorre dentro de outro caso de '
          'uso; a relação *extend* indica um comportamento opcional.'),
] + [('fig', k, 'Diagrama de casos de uso (%s).' % nome, D + 'casos-de-uso/%s.png' % arq, 6.0) for k, nome, arq in UC_FIGS] + [
    ('h3', 'Especificação dos casos de uso'),
    ('p', 'Os quadros a seguir detalham os casos de uso centrais do sistema: o acesso ({qd:uc01}), a venda de balcão '
          '({qd:uc26}), a geração da análise de previsão ({qd:uc38}) e a aplicação da recomendação de compra ({qd:uc41}).'),
    ('quadro', 'uc01', 'Caso de uso "Autenticar-se" (UC01).', [3.15, 3.15], [
        ['**Nome do caso de uso**', 'UC01 – Autenticar-se'],
        ['**Atores envolvidos**', 'Administrador.'],
        ['**Objetivo**', 'Permitir o acesso ao sistema por e-mail e senha, emitindo um token de acesso.'],
        ['H:Ações do ator', 'H:Ações do sistema'],
        ['1. O ator informa e-mail e senha e aciona "Entrar".', '2. O sistema busca o usuário pelo e-mail e confere a senha com o *hash* armazenado.'],
        ['', '3. Com a credencial válida e o usuário ativo, o sistema registra o último acesso e devolve o token JWT.'],
        ['4. O ator é direcionado ao painel, já com a loja de trabalho selecionada.', ''],
        ['**Fluxos alternativos**', 'E-mail inexistente ou senha incorreta: mensagem genérica "E-mail ou senha inválidos." (RN-AC03). Usuário inativo: acesso negado (RN-AC02).'],
        ['**Validações**', 'E-mail e senha obrigatórios. Todas as demais funcionalidades exigem o token.'],
    ]),
    ('quadro', 'uc26', 'Caso de uso "Realizar venda rápida" (UC26).', [3.15, 3.15], [
        ['**Nome do caso de uso**', 'UC26 – Realizar venda rápida (inclui: UC27 Buscar item, UC28 Registrar pagamentos)'],
        ['**Atores envolvidos**', 'Administrador.'],
        ['**Objetivo**', 'Registrar uma venda de balcão já paga, baixando o estoque do local de venda da loja.'],
        ['H:Ações do ator', 'H:Ações do sistema'],
        ['1. O ator lê o código de barras ou busca o produto por nome ou SKU.', '2. O sistema lista as variações com o preço efetivo, considerando a promoção vigente, e o disponível no local de venda.'],
        ['3. O ator ajusta as quantidades, informa o cliente (opcional) e as formas de pagamento.', '4. O sistema calcula subtotal, descontos, total, valor a pagar e troco, sem gravar.'],
        ['5. O ator conclui a venda.', '6. O sistema recalcula os preços, baixa cada item pelo livro-razão, a partir do lote que vence primeiro, e grava a venda, os itens e os pagamentos em uma única transação.'],
        ['**Fluxos alternativos**', 'Preço alterado desde a busca: o sistema pede confirmação do novo total. Estoque insuficiente: o sistema aponta os itens sem saldo e nada é gravado. Pagamentos que não fecham o total: erro no campo de pagamentos.'],
        ['**Validações**', 'RN-VD05, RN-CE15 e RN-CE32.'],
    ]),
    ('quadro', 'uc38', 'Caso de uso "Gerar análise de demanda" (UC38).', [3.15, 3.15], [
        ['**Nome do caso de uso**', 'UC38 – Gerar análise de demanda (inclui: UC39 Priorizar e explicar com a IA)'],
        ['**Atores envolvidos**', 'Administrador, Agendador e Serviço de IA.'],
        ['**Objetivo**', 'Projetar a demanda de cada produto e recomendar comprar, promover, transferir ou manter o estoque.'],
        ['H:Ações do ator', 'H:Ações do sistema'],
        ['1. O ator aciona "Gerar nova análise", ou o Agendador dispara a análise semanal.', '2. O sistema confere que não há outra análise em andamento, registra a nova análise e a coloca na fila de processamento em segundo plano.'],
        ['', '3. O motor recalcula os dados derivados (venda mensal, sazonalidade e fotografia diária do estoque), projeta a demanda e calcula a ação de cada produto.'],
        ['', '4. O sistema envia o resultado ao Serviço de IA em lotes sequenciais, aplica os limites à resposta e solicita um resumo geral.'],
        ['5. O ator acompanha o andamento na tela de previsão.', '6. O sistema grava as recomendações, expira as pendentes da análise anterior e notifica a conclusão.'],
        ['**Fluxos alternativos**', 'Análise em andamento: o sistema avisa e não inicia outra. IA indisponível ou sem chave: a análise é concluída apenas com o cálculo.'],
        ['**Validações**', 'RN-DF13, RN-DF14, RN-DF20 e RN-DF23.'],
    ]),
    ('quadro', 'uc41', 'Caso de uso "Aplicar Comprar" (UC41).', [3.15, 3.15], [
        ['**Nome do caso de uso**', 'UC41 – Aplicar Comprar (estendido por: UC42 Dividir a compra entre lojas)'],
        ['**Atores envolvidos**', 'Administrador.'],
        ['**Objetivo**', 'Transformar recomendações de compra em pedidos de compra em orçamento.'],
        ['H:Ações do ator', 'H:Ações do sistema'],
        ['1. O ator seleciona recomendações Comprar e aciona "Comprar".', '2. O sistema agrupa os itens por fornecedor, com a quantidade rateada nas variações, o último custo pago e, havendo duas ou mais lojas, a divisão sugerida por loja.'],
        ['3. O ator ajusta quantidades, custos e locais de entrega e confirma.', '4. O sistema valida cada item, cria um pedido em orçamento por fornecedor e loja e liga cada recomendação aos pedidos gerados, marcando-a como aplicada.'],
        ['5. O ator abre os pedidos gerados para revisão e envio ao fornecedor.', ''],
        ['**Fluxos alternativos**', 'Item inválido: erro na linha do item, sem gravar. Cancelamento de todos os pedidos gerados: a recomendação volta a pendente.'],
        ['**Validações**', 'RN-DF15, RN-DF27 e RN-DF28.'],
    ]),

    ('h2', 'Arquitetura do sistema'),
    ('p', 'O Nextflow segue o modelo cliente-servidor. O *frontend* é uma aplicação de página única em React com TypeScript, '
          'que apenas apresenta os dados e coleta as ações do usuário: preços, totais e regras de negócio são sempre '
          'calculados pela API. O *backend* é uma API REST em .NET 10, que persiste os dados no PostgreSQL por meio do Entity '
          'Framework Core, guarda as imagens em um serviço de armazenamento compatível com S3 e consulta o serviço de '
          'inteligência artificial Gemini, do Google (Google, s.d.).'),
    ('h3', 'Organização em camadas'),
    ('p', 'O *backend* foi estruturado segundo a *Clean Architecture* (Martin, 2019), em quatro camadas com dependências '
          'apontando para o domínio. A {fig:camadas} ilustra as camadas no fluxo da venda rápida:'),
    ('alineas', [
        ('API', 'controladores finos que recebem as requisições HTTP, exigem autenticação e devolvem as respostas em um formato padronizado, com os erros associados a cada campo do formulário;'),
        ('aplicação', 'um caso de uso por operação, com a validação dos dados de entrada e a orquestração do fluxo, gravando cada operação em uma única transação;'),
        ('domínio', 'entidades e regras de negócio, além das interfaces que a infraestrutura implementa, sem dependência de *frameworks*;'),
        ('infraestrutura', 'persistência com Entity Framework Core, livro-razão de estoque, armazenamento de arquivos, cliente do serviço de IA e processamento em segundo plano.'),
    ]),
    ('fig', 'camadas', 'Camadas da arquitetura no fluxo da venda rápida.', D + 'classes/classes-0-camadas.png', 6.3),
    ('h3', 'Decisões de arquitetura'),
    ('p', 'As decisões que mais influenciaram o desenho do sistema foram registradas pela equipe em documentos de decisão de '
          'arquitetura. As principais são:'),
    ('alineas', [
        ('estoque como livro-razão', 'o saldo não é um número editável, e sim a soma das movimentações, que nunca são alteradas nem apagadas; somente o serviço de livro-razão grava saldos e movimentações, o que preserva a auditoria e a integridade exigidas pelo RNF002;'),
        ('variação como unidade de estoque', 'venda, compra e saldo referem-se sempre à variação do produto (tamanho, sabor ou cor); um produto sem grade possui uma variação padrão oculta, de modo que todas as regras tratam um único caso;'),
        ('lojas e locais de estoque', 'cada loja possui locais, como a área de venda e o depósito, com um local padrão de venda e outro de recebimento; o saldo é mantido por variação, local e lote;'),
        ('o servidor calcula, a IA interpreta e o gestor decide', 'a previsão é calculada no servidor e a inteligência artificial apenas prioriza e explica, sob limites; nenhuma recomendação é aplicada sem a ação do gestor;'),
        ('processamento em segundo plano', 'a análise de previsão entra em uma fila e é executada por um serviço em segundo plano, uma por vez, com o andamento consultado pela tela;'),
        ('armazenamento de objetos', 'as imagens ficam em um serviço compatível com S3 e o banco guarda apenas a chave de cada arquivo, permitindo trocar de provedor sem alterar a aplicação.'),
    ]),

    ('h2', 'Modelo de domínio'),
    ('p', 'O modelo de domínio representa os conceitos do negócio e suas relações, independentemente da forma como são '
          'gravados no banco de dados. Os diagramas de classes a seguir foram elaborados em nível de análise: os nomes e '
          'atributos estão em português, com tipos simples, e as operações são as ações de negócio que alteram o estado da '
          'entidade, como enviar, receber e cancelar um pedido de compra. As ligações trazem o verbo e a multiplicidade, e o '
          'losango cheio indica composição, em que a parte só existe dentro do todo. Cada módulo tem uma cor, a mesma usada '
          'nos diagramas entidade-relacionamento.'),
    ('fig', 'dom1', 'Diagrama de classes: modelo de domínio (Acesso e cadastros).', D + 'classes/dominio-1-acesso-cadastros.png', 6.3),
    ('p', 'A {fig:dom2} apresenta o catálogo: o produto, suas variações e a grade de atributos, a classificação por categoria, '
          'coleção e eventos e o vínculo com fornecedores, que guarda o prazo, o pedido mínimo e o múltiplo de compra.'),
    ('fig', 'dom2', 'Diagrama de classes: modelo de domínio (Catálogo de produtos).', D + 'classes/dominio-2-catalogo.png', 6.3),
    ('p', 'A {fig:dom3} mostra a decisão central do sistema: o saldo de cada variação em cada local e lote resulta das '
          'movimentações do livro-razão.'),
    ('fig', 'dom3', 'Diagrama de classes: modelo de domínio (Estoque).', D + 'classes/dominio-3-estoque.png', 6.3),
    ('p', 'Nas vendas ({fig:dom4}), a venda é dona dos seus itens e pagamentos; nas compras ({fig:dom5}), o ciclo de vida do '
          'pedido é controlado pelas operações enviar, receber e cancelar.'),
    ('fig', 'dom4', 'Diagrama de classes: modelo de domínio (Vendas e promoções).', D + 'classes/dominio-4-vendas.png', 6.0),
    ('fig', 'dom5', 'Diagrama de classes: modelo de domínio (Compras).', D + 'classes/dominio-5-compras.png', 5.5),
    ('p', 'A {fig:dom6} apresenta a previsão: a análise gera recomendações, a IA atua sobre lotes de produtos e a aplicação '
          'liga a recomendação ao que ela gerou. A {fig:dom7} mostra os dados derivados que alimentam o cálculo.'),
    ('fig', 'dom6', 'Diagrama de classes: modelo de domínio (Previsão de demanda com IA).', D + 'classes/dominio-6-previsao.png', 6.3),
    ('fig', 'dom7', 'Diagrama de classes: modelo de domínio (Dados que alimentam a previsão).', D + 'classes/dominio-7-dados-previsao.png', 6.3),

    ('h2', 'Modelo de dados'),
    ('p', 'O Diagrama Entidade-Relacionamento (DER) é a representação gráfica do modelo entidade-relacionamento proposto por '
          'Chen (1976), que descreve os dados por meio de entidades, atributos e relacionamentos. O banco de dados do '
          'Nextflow possui 48 tabelas e 82 chaves estrangeiras, distribuídas em 11 figuras por módulo; o mapa geral fica no '
          'apêndice.'),
    ('h3', 'Diagramas entidade-relacionamento'),
    ('p', 'Em cada figura, a tabela traz o nome em português e, entre parênteses, o nome no banco de dados; cada coluna '
          'mostra o tipo, a chave (PK primária e FK estrangeira) e um comentário. As ligações são lidas a partir da tabela que '
          'possui a chave primária, com o verbo da relação, e a linha tracejada indica uma ligação sem chave estrangeira '
          'física, como a de endereços e contatos, que podem pertencer a um cliente ou a um fornecedor. As colunas de '
          'auditoria, presentes em quase todas as tabelas, foram omitidas.'),
    ('fig', 'der1', 'Diagrama entidade-relacionamento (Acesso e notificações).', D + 'der/der-1-acesso.png', 5.0),
    ('fig', 'der2', 'Diagrama entidade-relacionamento (Cadastros de pessoas e localidade).', D + 'der/der-2-cadastros.png', 6.3),
    ('fig', 'der3', 'Diagrama entidade-relacionamento (Produto, variações e preço).', D + 'der/der-3-produto.png', 6.3),
    ('fig', 'der4', 'Diagrama entidade-relacionamento (Classificação e fornecimento do produto).', D + 'der/der-4-classificacao.png', 6.3),
    ('p', 'A {fig:der5} registra as decisões de estoque: o saldo por variação, local e lote e o livro-razão, cujas '
          'movimentações apontam para o documento de origem (venda, pedido de compra, transferência ou ajuste).'),
    ('fig', 'der5', 'Diagrama entidade-relacionamento (Lojas, locais, saldo e livro-razão).', D + 'der/der-5-estoque.png', 6.3),
    ('fig', 'der6', 'Diagrama entidade-relacionamento (Transferência de estoque).', D + 'der/der-6-transferencia.png', 6.3),
    ('fig', 'der7', 'Diagrama entidade-relacionamento (Vendas e promoções).', D + 'der/der-7-vendas.png', 6.3),
    ('fig', 'der8', 'Diagrama entidade-relacionamento (Pedidos de compra).', D + 'der/der-8-compras.png', 6.3),
    ('p', 'As figuras {fig:der9} e {fig:der10} tratam da previsão: a análise, as recomendações, os lotes enviados à IA e as '
          'projeções, e a ligação de cada recomendação com o que ela gerou, incluindo a parte de cada loja e de cada '
          'variação. A {fig:der11} apresenta os dados derivados, recalculados a partir das vendas e do estoque.'),
    ('fig', 'der9', 'Diagrama entidade-relacionamento (Previsão: análise e recomendação).', D + 'der/der-9-previsao-analise.png', 6.3),
    ('fig', 'der10', 'Diagrama entidade-relacionamento (Previsão: aplicação da recomendação).', D + 'der/der-10-previsao-aplicacao.png', 6.3),
    ('fig', 'der11', 'Diagrama entidade-relacionamento (Dados derivados para a previsão).', D + 'der/der-11-dados-derivados.png', 6.3),
    ('h3', 'Dicionário de dados'),
    ('p', 'O Dicionário de Dados (DD) descreve os elementos de dados do sistema. Os quadros a seguir apresentam as tabelas '
          'centrais do estoque e das vendas, com os campos Atributo, Classe, Domínio, Tamanho e Descrição; no domínio, PK '
          'indica chave primária, FK chave estrangeira, NN não nulo e UN único. As colunas de data de criação e de '
          'alteração foram omitidas, exceto quando têm significado de negócio.'),
    ('dd', 'ddprod', 'products', {
        'id': 'Identificador único do produto.',
        'name': 'Nome comercial do produto.',
        'brand': 'Marca (opcional).',
        'description': 'Descrição do produto (opcional).',
        'product_type': 'Tipo: padrão, vestuário, perecível ou granel.',
        'sale_unit': 'Unidade de venda: unidade, quilograma, litro ou metro.',
        'decimal_places': 'Casas decimais aceitas na quantidade.',
        'allows_negative': 'Indica se o estoque pode ficar negativo.',
        'has_variants': 'Indica se o produto possui grade de variações.',
        'tracks_lots': 'Indica se o produto controla lote e validade.',
        'shelf_life_days': 'Vida útil em dias (opcional).',
        'collection_id': 'Coleção do produto (opcional).',
        'lifecycle': 'Ciclo de vida: em linha ou fora de linha.',
        'launched_on': 'Data de lançamento (opcional).',
        'image_key': 'Chave da foto no armazenamento de objetos (opcional).',
        'is_active': 'Indica se o produto está ativo.',
        'abc_class': 'Classe ABC atribuída pela análise (opcional).',
        'default_min_quantity': 'Estoque mínimo padrão por local.',
        'target_coverage_days': 'Cobertura alvo em dias, quando difere da política da classe (opcional).',
    }),
    ('dd', 'ddvar', 'product_variants', {
        'id': 'Identificador único da variação.',
        'product_id': 'Produto ao qual a variação pertence.',
        'sku': 'Código interno da variação (SKU).',
        'barcode': 'Código de barras (opcional).',
        'price': 'Preço de venda da variação.',
        'sort_order': 'Ordem de exibição na grade.',
        'is_active': 'Indica se a variação está ativa.',
        'removed_on': 'Data em que saiu da grade (opcional).',
        'average_cost': 'Custo médio ponderado (opcional).',
        'last_cost': 'Último custo de compra (opcional).',
        'version': 'Controle de concorrência na atualização do custo médio.',
    }),
    ('dd', 'ddsaldo', 'stock_balances', {
        'id': 'Identificador único do saldo.',
        'variant_id': 'Variação do produto.',
        'location_id': 'Local de estoque.',
        'lot_id': 'Lote (opcional); a combinação variação, local e lote é única.',
        'quantity': 'Saldo atual, igual à soma das movimentações.',
        'version': 'Controle de concorrência na atualização do saldo.',
    }),
    ('dd', 'ddmov', 'stock_movements', {
        'id': 'Identificador único da movimentação.',
        'variant_id': 'Variação movimentada.',
        'location_id': 'Local de estoque.',
        'lot_id': 'Lote (opcional).',
        'type': 'Sentido: entrada ou saída.',
        'reason': 'Motivo: abertura, compra, venda, transferência, ajuste, quebra, vencimento, entre outros.',
        'quantity': 'Quantidade movimentada.',
        'unit_cost': 'Custo unitário (opcional).',
        'balance_after': 'Saldo após a movimentação.',
        'source_type': 'Tipo do documento de origem: venda, pedido de compra, transferência ou manual.',
        'source_id': 'Documento de origem (opcional).',
        'user_id': 'Usuário que registrou a movimentação.',
        'note': 'Observação (opcional).',
        'created_at': 'Data e hora da movimentação.',
    }),
    ('dd', 'ddvenda', 'orders', {
        'id': 'Identificador único da venda.',
        'number': 'Número sequencial da venda.',
        'store_id': 'Loja da venda.',
        'sale_location_id': 'Local de onde o estoque foi baixado.',
        'client_id': 'Cliente (opcional).',
        'user_id': 'Usuário que realizou a venda.',
        'status': 'Situação da venda.',
        'channel': 'Canal de venda (balcão).',
        'subtotal': 'Soma dos itens antes dos descontos.',
        'discount_total': 'Total de descontos.',
        'total': 'Valor total da venda.',
        'cash_received': 'Valor recebido em dinheiro (opcional).',
        'change': 'Troco (opcional).',
        'paid_at': 'Data e hora do pagamento (opcional).',
    }),
    ('dd', 'dditem', 'order_items', {
        'id': 'Identificador único do item.',
        'order_id': 'Venda à qual o item pertence.',
        'position': 'Posição do item na venda.',
        'variant_id': 'Variação vendida.',
        'quantity': 'Quantidade vendida.',
        'list_price': 'Preço de tabela no momento da venda.',
        'unit_price': 'Preço praticado, com a promoção aplicada.',
        'discount': 'Desconto do item.',
        'line_total': 'Total do item.',
        'promotion_id': 'Promoção aplicada (opcional).',
        'unit_cost': 'Custo médio registrado na baixa (opcional).',
    }),

    ('h2', 'Diagramas de sequência'),
    ('p', 'Os diagramas de sequência mostram, em ordem cronológica, a troca de mensagens entre o usuário, o *frontend*, a API, '
          'os serviços internos e o banco de dados nos fluxos principais. Os participantes estão agrupados por camada, os '
          'passos são numerados para facilitar a leitura e as faixas indicam as fases de cada fluxo; os blocos *alt* '
          'representam caminhos alternativos, *opt* passos condicionais e *loop* repetições. O livro-razão de estoque aparece '
          'como participante próprio por ser o único caminho que altera saldos, e o motor da previsão por ser executado em '
          'segundo plano.'),
    ('fig', 'seq1', 'Diagrama de sequência (Autenticação e painel).', D + 'sequencia/seq-1-autenticacao-painel.png', 6.3),
    ('p', 'Na {fig:seq1}, depois da autenticação, o painel carrega em paralelo os indicadores de vendas, os alertas de '
          'estoque e as recomendações, sempre com o token e a loja selecionada.'),
    ('fig', 'seq2', 'Diagrama de sequência (Venda rápida no balcão).', D + 'sequencia/seq-2-venda-rapida.png', 6.3),
    ('p', 'Na venda rápida ({fig:seq2}), o preço vem sempre da API, a baixa passa pelo livro-razão e a venda é gravada em uma '
          'única transação: se algum item não tiver saldo, nada é gravado.'),
    ('fig', 'seq3', 'Diagrama de sequência (Pedido de compra: criar, enviar e receber).', D + 'sequencia/seq-3-compra.png', 6.3),
    ('p', 'A {fig:seq3} percorre o ciclo do pedido de compra, de orçamento a pendente e a recebido; é o recebimento que '
          'lança a mercadoria no estoque e atualiza o custo médio. A {fig:seq4} mostra o ajuste manual e a transferência '
          'entre locais, que repete na entrada os mesmos lotes que saíram da origem.'),
    ('fig', 'seq4', 'Diagrama de sequência (Ajuste e transferência de estoque).', D + 'sequencia/seq-4-estoque.png', 6.3),
    ('fig', 'seq5', 'Diagrama de sequência (Análise de previsão de demanda).', D + 'sequencia/seq-5-analise-previsao.png', 6.3),
    ('p', 'A {fig:seq5} detalha a análise de previsão, descrita na seção seguinte, e a {fig:seq6} a transformação das '
          'recomendações de compra em pedidos em orçamento, um por fornecedor e loja. Por fim, a {fig:seq7} mostra a '
          'sugestão pedida na hora a partir do painel, que abre o pedido de compra já preenchido.'),
    ('fig', 'seq6', 'Diagrama de sequência (Aplicar recomendação Comprar).', D + 'sequencia/seq-6-aplicar-comprar.png', 6.3),
    ('fig', 'seq7', 'Diagrama de sequência (Sugestão da IA a partir do painel).', D + 'sequencia/seq-7-sugestao-ia.png', 6.3),

    ('h2', 'Previsão de demanda'),
    ('p', 'O módulo de previsão de demanda é o diferencial do Nextflow. Ele combina um cálculo estatístico, executado no '
          'servidor, com a revisão por um modelo de inteligência artificial generativa, e entrega ao gestor recomendações '
          'acompanhadas dos números que as justificam.'),
    ('h3', 'Dados de entrada'),
    ('p', 'A análise parte das vendas pagas, agregadas por mês e por produto. Para não recalcular o histórico inteiro a cada '
          'consulta, o sistema mantém três conjuntos de dados derivados, recalculados no início de cada análise: a venda '
          'mensal de cada produto, que registra também a quantidade vendida em promoção e os dias sem estoque; a fotografia '
          'diária do estoque; e o índice de sazonalidade de cada produto. Registrar os dias sem estoque evita que um mês de '
          'ruptura, em que se vendeu pouco por falta de mercadoria, seja interpretado como queda de demanda.'),
    ('p', 'Somam-se a esses dados o estoque atual, as quantidades a caminho em pedidos de compra pendentes, o prazo de '
          'entrega de cada fornecedor (a média real dos recebimentos ou, na falta dela, o prazo cadastrado), o pedido mínimo e '
          'o múltiplo de compra, a vida útil dos produtos, as datas do calendário comercial e a política de cobertura de cada '
          'classe ABC.'),
    ('h3', 'Cálculo da demanda e da necessidade'),
    ('p', 'O horizonte da análise é definido automaticamente como o maior prazo de entrega entre os produtos acrescido de '
          'três meses, com limite de seis meses. Para cada produto, o sistema calcula índices sazonais mensais, que expressam '
          'quanto cada mês vende em relação à média, seguindo a ideia da decomposição de séries temporais em tendência e '
          'sazonalidade (Hyndman; Athanasopoulos, 2021). Produtos com pouco histórico têm o índice combinado com o da '
          'categoria, com peso proporcional aos meses disponíveis, e o índice é limitado para evitar valores extremos. Um '
          'produto sazonal sem vendas recentes, como um item de Páscoa fora de época, é projetado pelo mesmo mês do ano '
          'anterior, corrigido pela tendência.'),
    ('p', 'Com a demanda projetada, a necessidade de compra é a demanda prevista para o prazo de entrega acrescido de 30 '
          'dias, somada ao estoque de segurança e descontados o estoque atual e o que está a caminho; o resultado é '
          'arredondado ao pedido mínimo e ao múltiplo do fornecedor. A partir desses números, cada produto recebe uma ação:'),
    ('alineas', [
        ('Comprar', 'quando há necessidade de reposição dentro da janela de compra;'),
        ('Promover', 'quando há excesso de estoque em baixa temporada ou um lote próximo do vencimento com sobra; o desconto sugerido preserva uma margem mínima sobre o custo;'),
        ('Transferir', 'quando um local está abaixo do mínimo e outro local da empresa tem excesso da mesma variação, situação em que transferir evita uma compra;'),
        ('Manter', 'quando o estoque atende à demanda prevista; se a previsão for zero na janela de compra, a recomendação indica que não há ação a tomar.'),
    ]),
    ('p', 'Cada recomendação traz ainda uma prioridade e uma confiança, que depende da quantidade de meses de histórico, e a '
          'quantidade do produto é distribuída entre as variações na proporção histórica de venda da grade.'),
    ('h3', 'Papel da inteligência artificial'),
    ('p', 'Concluído o cálculo, o sistema envia os resultados ao modelo Gemini, do Google, em lotes sequenciais de até 40 '
          'produtos, solicitando uma resposta estruturada em JSON (Google, s.d.). Para cada produto, a IA pode ajustar a '
          'prioridade, refinar a quantidade ou o desconto e redigir uma explicação em português. Ao final, uma última chamada '
          'produz o resumo geral da análise.'),
    ('p', 'A resposta passa por limites antes de ser gravada: a quantidade de compra fica entre 0,5 e 1,5 vez a calculada, o '
          'desconto respeita a margem mínima e a duração da promoção fica entre 7 e 45 dias. A IA não altera a confiança, não '
          'transforma em compra um produto sem necessidade calculada e não cria uma promoção ou uma transferência sem que o '
          'cálculo tenha encontrado o motivo correspondente. Se o serviço falhar, estiver indisponível ou sem chave '
          'configurada, o lote afetado permanece com o resultado do cálculo e com motivos gerados por modelo de texto, e a '
          'análise é concluída normalmente. Nenhum dado pessoal de clientes é enviado ao serviço.'),
    ('h3', 'Execução e aplicação das recomendações'),
    ('p', 'A análise é executada em segundo plano, uma por vez, pelo botão "Gerar nova análise" ou automaticamente uma vez '
          'por semana, no dia e horário configurados. A tela acompanha o andamento dos lotes e, ao final, o sistema gera uma '
          'notificação. Uma nova análise expira as recomendações ainda pendentes da anterior.'),
    ('p', 'O gestor decide o que fazer com cada recomendação: aplicar Comprar gera pedidos de compra em orçamento, um por '
          'fornecedor e por loja, que ainda precisam ser enviados ao fornecedor; aplicar Promover cria a promoção sugerida; '
          'aplicar Transferir registra a transferência entre os locais; e descartar exige um motivo. Além da análise completa, '
          'o painel permite pedir na hora uma sugestão de compra para um item com estoque baixo ou de desconto para um lote '
          'próximo do vencimento.'),
    ('h3', 'Medição da precisão'),
    ('p', 'Para avaliar a previsão, o sistema compara, a cada mês encerrado, a demanda projetada pela última análise feita '
          'antes desse mês com a quantidade efetivamente vendida. A medida utilizada é o erro percentual absoluto médio (MAPE, '
          'do inglês *mean absolute percentage error*), uma das medidas de acurácia descritas por Hyndman e Athanasopoulos '
          '(2021). Um produto é considerado dentro da tolerância quando o MAPE é de até 15%, e a tendência de a previsão ficar '
          'abaixo ou acima do vendido só é apontada quando o erro médio com sinal passa de 5%. Meses em que o produto ficou '
          'sem estoque em mais da metade dos dias são excluídos da medição, pois a venda registrada não representa a demanda.'),

    ('h2', 'Interfaces de usuário'),
    ('p', 'A interface foi desenvolvida em React com os componentes do *shadcn/ui*, com temas claro e escuro e layout que se '
          'adapta ao celular. Em todas as telas, a barra lateral dá acesso aos módulos e o topo mantém o seletor da loja de '
          'trabalho e o sino de notificações. As telas a seguir foram capturadas com os dados de demonstração de uma loja de '
          'doces e presentes com duas unidades.'),
    ('p', 'A {fig:tlogin} apresenta a tela de login, composta pelos campos de e-mail e senha e pelo botão "Entrar".'),
    ('fig', 'tlogin', 'Tela de login.', S + 'light/00-login.png', 6.0),
    ('p', 'A {fig:tpainel} mostra o painel inicial, composto por:'),
    ('alineas', [
        ('indicadores do mês', 'faturamento, pedidos pagos, ticket médio e margem bruta, comparados com o mês e o ano anteriores;'),
        ('recomendações da IA', 'resumo da última análise e as cinco recomendações de maior prioridade, com a ação, o motivo e a quantidade ou o desconto sugerido;'),
        ('faturamento por mês', 'gráfico dos últimos doze meses comparados com o mesmo período do ano anterior;'),
        ('alertas', 'estoque baixo, lotes que vencem nos próximos 30 dias e próximas datas comerciais, com acesso à lista completa.'),
    ]),
    ('fig', 'tpainel', 'Painel inicial.', S + 'light/01-painel.png', 6.3),
    ('p', 'A {fig:tproduto} exibe a visualização de um produto, com a foto, o tipo, a classificação, o custo médio, a margem '
          'e o disponível nas lojas; as abas reúnem as variações, o estoque por local, os lotes, os fornecedores, o histórico '
          'de preços, as promoções e a previsão do produto.'),
    ('fig', 'tproduto', 'Visualização de produto.', S + 'light/52-produto-visualizar.png', 6.3),
    ('p', 'A {fig:tlojas} apresenta o cadastro de lojas e locais: cada loja lista seus locais, se são vendáveis e qual é o '
          'local padrão de venda e de recebimento.'),
    ('fig', 'tlojas', 'Lojas e locais de estoque.', S + 'light/70-lojas-e-locais.png', 6.3),
    ('p', 'A {fig:tmov} mostra as movimentações de estoque, o livro-razão do sistema: cada linha registra data, produto, '
          'local, lote, motivo, quantidade, custo unitário, saldo após a movimentação, documento de origem e usuário.'),
    ('fig', 'tmov', 'Movimentações de estoque.', S + 'light/57-movimentacoes.png', 6.3),
    ('p', 'A {fig:tvenda} apresenta a venda rápida, com a busca por nome, SKU ou código de barras à esquerda e, à direita, o '
          'cliente opcional, as formas de pagamento e o resumo, cujos valores são calculados pela API. A {fig:tvendacel} '
          'mostra a mesma tela no celular.'),
    ('fig', 'tvenda', 'Venda rápida.', S + 'light/20-venda-rapida.png', 6.3),
    ('fig', 'tvendacel', 'Venda rápida no celular.', S + 'mobile/20-venda-rapida.png', 2.4),
    ('p', 'A {fig:tcompras} exibe a listagem de pedidos de compra, com filtro de situação, o local de entrega, o total, a '
          'previsão de chegada e o destaque para os pedidos atrasados.'),
    ('fig', 'tcompras', 'Pedidos de compra.', S + 'light/30-pedidos-compra.png', 6.3),
    ('p', 'A {fig:tprev} apresenta a tela de previsão de demanda, com os dados da última análise, o resumo produzido pela IA, '
          'as abas por ação e a lista de recomendações com estoque, cobertura, demanda no horizonte, sugestão e fornecedor. '
          'Ao abrir uma recomendação ({fig:tprevdet}), o gestor vê o motivo escrito pela IA ao lado do motivo calculado, os '
          'números do cálculo e as ações disponíveis.'),
    ('fig', 'tprev', 'Previsão de demanda.', S + 'light/10-previsao.png', 6.3),
    ('fig', 'tprevdet', 'Detalhe de uma recomendação.', S + 'light/11-previsao-detalhe.png', 6.3),
    ('h3', 'Acessibilidade'),
    ('p', 'Os componentes do *shadcn/ui* são construídos sobre primitivas que seguem as práticas de acessibilidade para '
          'navegação por teclado e leitores de tela. A interface utiliza contraste adequado nos dois temas, rótulos em todos '
          'os campos, mensagens de erro junto ao campo correspondente e hierarquia visual consistente, buscando reduzir a '
          'carga cognitiva do usuário no uso diário.'),
]

# Referência nova (entra depois de FIELDING, em ordem alfabética)
REFERENCIAS = [
    ('FIELDING, Roy Thomas', 'GOOGLE. **Gemini API documentation**. [S. l.], [s.d.]. Disponível em: https://ai.google.dev/gemini-api/docs. Acesso em: 09 nov. 2026.'),
]
