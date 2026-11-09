"""Pré e pós-textuais do TCC, depois dos capítulos (último passo do montar.sh).

Uso: python3 -I pretextuais.py <entrada.odt> <saida.odt>

- Folha de aprovação, resumo, abstract e palavras-chave (texto novo em verde).
- Listas de figuras e de quadros e o sumário: gerados a partir das legendas e dos títulos do próprio documento.
- Lista de siglas: só as siglas que aparecem no texto, da tabela SIGLAS abaixo.
- Apêndice A: mapa geral do modelo de dados.
- Confere citações × referências e imprime o que não bate (não altera nada).
"""
import os, re, sys, struct, zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
src, dst = sys.argv[1:3]
zin = zipfile.ZipFile(src)
x = zin.read('content.xml').decode('utf-8')
manifest = zin.read('META-INF/manifest.xml').decode('utf-8')
HL = 'TccNovo'

DATA_APROVACAO = 'Americana, ___ de dezembro de 2026.'

RESUMO = ('O presente trabalho aborda o desenvolvimento do Nextflow, um sistema web de gestão para comércios de pequeno e '
          'médio porte que integra o catálogo de produtos, o estoque, as vendas de balcão e as compras a um módulo de '
          'previsão de demanda com apoio de inteligência artificial. O problema que motivou a pesquisa é a gestão de '
          'estoque baseada na memória ou em planilhas, que leva a compras sem base em dados, à falta de produtos nas datas '
          'de maior venda e a mercadoria parada ou vencida. O objetivo foi desenvolver um sistema modular e acessível que '
          'mantenha registros confiáveis do estoque e apoie a decisão de compra. A metodologia fundamentou-se no '
          'desenvolvimento ágil e incremental, com a *Clean Architecture* no *backend* em .NET 10, interface em React com '
          'TypeScript, banco de dados PostgreSQL e execução em contêineres Docker. O estoque é registrado como um '
          'livro-razão, em que o saldo é sempre a soma de movimentações que não podem ser alteradas, e a previsão projeta a '
          'demanda de cada produto a partir do histórico de vendas e da sazonalidade, recomendando comprar, promover, '
          'transferir entre lojas ou manter o estoque; um modelo de inteligência artificial generativa apenas prioriza e '
          'explica as recomendações, dentro de limites, e a decisão permanece com o gestor. Os resultados, obtidos com três '
          'anos de dados de demonstração de uma loja de doces e presentes, mostram recomendações coerentes com a '
          'sazonalidade, consultas respondidas em média em menos de 100 milissegundos e 1.059 testes automatizados '
          'aprovados. Conclui-se que o Nextflow oferece aos pequenos comércios uma ferramenta acessível para controlar o '
          'estoque e decidir o que comprar com base em dados.')
PALAVRAS = 'Gestão de estoques; previsão de demanda; inteligência artificial; sistemas de informação; pequenas empresas.'

ABSTRACT = ('This work presents the development of Nextflow, a web-based management system for small and medium-sized '
            'retailers that integrates the product catalog, inventory, counter sales and purchasing with a demand '
            'forecasting module supported by artificial intelligence. The problem that motivated the research is inventory '
            'management based on memory or spreadsheets, which leads to purchases without supporting data, stockouts on '
            'peak sales dates and idle or expired goods. The objective was to develop a modular and accessible system that '
            'keeps reliable inventory records and supports purchasing decisions. The methodology was based on agile, '
            'incremental development, using Clean Architecture in a .NET 10 backend, a React and TypeScript interface, a '
            'PostgreSQL database and Docker containers. Inventory is recorded as a ledger, in which the balance is always '
            'the sum of movements that cannot be changed, and the forecast projects the demand for each product from sales '
            'history and seasonality, recommending to buy, promote, transfer between stores or keep the stock; a generative '
            'artificial intelligence model only prioritizes and explains the recommendations, within limits, and the '
            'decision remains with the manager. The results, obtained with three years of demonstration data from a candy '
            'and gift store, show recommendations consistent with seasonality, queries answered on average in less than '
            '100 milliseconds and 1,059 automated tests passing. It is concluded that Nextflow offers small retailers an '
            'accessible tool to control inventory and decide what to buy based on data.')
KEYWORDS = 'Inventory management; demand forecasting; artificial intelligence; information systems; small businesses.'

# sigla: (expansão em português, termo em inglês ou None). Entra na lista só se aparecer no texto.
SIGLAS = {
    'ANPD': ('Autoridade Nacional de Proteção de Dados', None),
    'API': ('Interface de Programação de Aplicações', 'Application Programming Interface'),
    'CEP': ('Código de Endereçamento Postal', None),
    'DD': ('Dicionário de Dados', 'Data Dictionary'),
    'DDD': ('Design Orientado a Domínio', 'Domain-Driven Design'),
    'DER': ('Diagrama Entidade-Relacionamento', 'Entity-Relationship Diagram'),
    'ERP': ('Planejamento de Recursos Empresariais', 'Enterprise Resource Planning'),
    'FEFO': ('Primeiro que Vence, Primeiro que Sai', 'First Expired, First Out'),
    'FK': ('Chave Estrangeira', 'Foreign Key'),
    'HTTP': ('Protocolo de Transferência de Hipertexto', 'Hypertext Transfer Protocol'),
    'IA': ('Inteligência Artificial', 'Artificial Intelligence'),
    'IBGE': ('Instituto Brasileiro de Geografia e Estatística', None),
    'JSON': ('Notação de Objetos JavaScript', 'JavaScript Object Notation'),
    'JWT': ('Token Web JSON', 'JSON Web Token'),
    'LGPD': ('Lei Geral de Proteção de Dados Pessoais', None),
    'LTS': ('Suporte de Longo Prazo', 'Long-Term Support'),
    'MAPE': ('Erro Percentual Absoluto Médio', 'Mean Absolute Percentage Error'),
    'MPE': ('Micro e Pequenas Empresas', None),
    'MRP I': ('Planejamento de Necessidades de Materiais', 'Material Requirements Planning'),
    'MRP II': ('Planejamento de Recursos de Manufatura', 'Manufacturing Resource Planning'),
    'NIST': ('Instituto Nacional de Padrões e Tecnologia dos Estados Unidos', 'National Institute of Standards and Technology'),
    'NN': ('Não Nulo', 'Not Null'),
    'ORM': ('Mapeamento Objeto-Relacional', 'Object-Relational Mapping'),
    'OWASP': ('Projeto Aberto Mundial de Segurança de Aplicações', 'Open Worldwide Application Security Project'),
    'PK': ('Chave Primária', 'Primary Key'),
    'RBAC': ('Controle de Acesso Baseado em Função', 'Role-Based Access Control'),
    'REST': ('Transferência de Estado Representacional', 'Representational State Transfer'),
    'RF': ('Requisito Funcional', None),
    'RNF': ('Requisito Não Funcional', None),
    'S3': ('Serviço Simples de Armazenamento', 'Simple Storage Service'),
    'SGBD': ('Sistema Gerenciador de Banco de Dados', None),
    'SKU': ('Unidade de Manutenção de Estoque', 'Stock Keeping Unit'),
    'SUS': ('Escala de Usabilidade do Sistema', 'System Usability Scale'),
    'UC': ('Caso de Uso', 'Use Case'),
    'UML': ('Linguagem de Modelagem Unificada', 'Unified Modeling Language'),
    'UN': ('Único', 'Unique'),
    'UUID': ('Identificador Único Universal', 'Universally Unique Identifier'),
    'UX': ('Experiência do Usuário', 'User Experience'),
    'WCAG': ('Diretrizes de Acessibilidade para Conteúdo Web', 'Web Content Accessibility Guidelines'),
    'XML': ('Linguagem de Marcação Extensível', 'Extensible Markup Language'),
}

# ---------- utilitários ----------
def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def text_xml(s):
    s = esc(s)
    s = re.sub(r'  +', lambda m: ' ' + '<text:s text:c="%d"/>' % (len(m.group(0)) - 1), s)
    if s.startswith(' '):
        s = '<text:s/>' + s[1:]
    if s.endswith(' '):
        s = s[:-1] + '<text:s/>'
    return s

def runs(s, base='TcT', ital='TcI'):
    out = []
    for part in re.split(r'(\*[^*]+\*)', s):
        if not part:
            continue
        st, t = (ital, part[1:-1]) if part.startswith('*') else (base, part)
        out.append('<text:span text:style-name="%s"><text:span text:style-name="%s">%s</text:span></text:span>' % (st, HL, text_xml(t)))
    return ''.join(out)

def plain(p):
    p = re.sub(r'<text:s(?: text:c="(\d+)")?/>', lambda m: ' ' * int(m.group(1) or 1), p)
    p = p.replace('<text:tab/>', '\t').replace('<text:line-break/>', ' ')
    return re.sub(r'<[^>]+>', '', p).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')

def para_at(key, start=0):
    """(início, fim) do parágrafo cujo texto contém key (único a partir de start)."""
    hits = [m for m in re.compile(r'<text:(p|h)\b[^>]*?(?:/>|>.*?</text:\1>)', re.S).finditer(x, start) if key in plain(m.group(0))]
    if len(hits) != 1:
        raise SystemExit('parágrafo %r: %d ocorrências' % (key, len(hits)))
    return hits[0].start(), hits[0].end()

def set_para_text(key, new_inner, keep_open=True):
    global x
    a, b = para_at(key)
    p = x[a:b]
    open_tag = re.match(r'<text:(?:p|h)\b[^>]*>', p).group(0)
    close = '</text:h>' if p.startswith('<text:h') else '</text:p>'
    x = x[:a] + open_tag + new_inner + close + x[b:]

# ---------- folha de aprovação, resumo, abstract ----------
set_para_text('18 de junho de 2021', runs(DATA_APROVACAO))
set_para_text('O presente trabalho aborda o desenvolvimento do Nextflow', runs(RESUMO))
set_para_text('This work addresses the development of Nextflow', runs(ABSTRACT, 'TcEn', 'TcEnI'))
set_para_text('Palavras-chave:', '<text:span text:style-name="TcB">Palavras-chave:</text:span>' + runs(' ' + PALAVRAS))
set_para_text('Keywords:', '<text:span text:style-name="TcEnB">Keywords:</text:span>' + runs(' ' + KEYWORDS, 'TcEn', 'TcEnI'))
extra = ('<style:style style:name="TcEn" style:family="text"><style:text-properties fo:language="en" fo:country="US"/></style:style>'
         '<style:style style:name="TcEnI" style:family="text"><style:text-properties fo:font-style="italic" style:font-style-asian="italic" style:font-style-complex="italic" fo:language="en" fo:country="US"/></style:style>'
         '<style:style style:name="TcEnB" style:family="text"><style:text-properties fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold" fo:language="en" fo:country="US"/></style:style>')
if 'style:name="TcEn"' not in x:
    x = x.replace('<office:automatic-styles>', '<office:automatic-styles>' + extra, 1)

# ---------- corpo do documento (depois do sumário) ----------
def body_start():
    return x.find('</text:table-of-content>')

def captions(kind):
    out = []
    for m in re.finditer(r'<text:p text:style-name="P916">(.*?)</text:p>', x[body_start():], re.S):
        t = plain(m.group(1)).strip()
        if t.startswith(kind + ' '):
            out.append(t)
    return out

def replace_entries(title_key, next_key, lines, entry_builder):
    """Troca os parágrafos entre o título da lista e os parágrafos vazios que antecedem o título seguinte."""
    global x
    a = para_at(title_key)[1]
    b = para_at(next_key)[0]
    seg = x[a:b]
    # mantém os parágrafos vazios do fim (espaçamento antes do próximo título)
    tail = re.search(r'(?:<text:p text:style-name="[^"]+"/>)*$', seg).group(0)
    head = re.match(r'(?:<text:p text:style-name="[^"]+"/>)*', seg).group(0)
    x = x[:a] + head + ''.join(entry_builder(l) for l in lines) + tail + x[b:]

def lista_entry(style):
    def build(line):
        return '<text:p text:style-name="%s">%s<text:span text:style-name="TcT"><text:tab/></text:span></text:p>' % (style, runs(line))
    return build

# ---------- apêndice A ----------
APX_TITULO = 'APÊNDICE A – MAPA GERAL DO MODELO DE DADOS'
APX_IMG = os.path.normpath(os.path.join(HERE, '../../docs/architecture/diagrams/uml/der/der-apendice-geral.png'))
a, b = para_at('APÊNDICE A –', x.find('</text:table-of-content>'))
h = x[a:b]
h = re.sub(r'>APÊNDICE A –[^<]*<', '><text:span text:style-name="%s">%s</text:span><' % (HL, APX_TITULO), h, count=1)
with open(APX_IMG, 'rb') as f:
    w, hh = struct.unpack('>II', f.read(24)[16:24])
height = 8.2
width = height * w / hh
if width > 6.3:
    width = 6.3; height = width * hh / w
img_name = 'media/tcc_apendice_der-geral.png'
fig = ('<text:p text:style-name="P916">%s</text:p><text:p text:style-name="P1137"><draw:frame draw:style-name="TcFig" '
       'draw:name="apendiceA" text:anchor-type="as-char" svg:width="%.3fin" svg:height="%.3fin" draw:z-index="0">'
       '<draw:image xlink:href="%s" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/></draw:frame></text:p>'
       '<text:p text:style-name="P1138">%s%s</text:p>') % (
    runs('Figura %d – Mapa geral do modelo de dados.' % (len(captions('Figura')) + 1), 'TcL', 'TcLI'), width, height, img_name,
    runs('Fonte:', 'TcLB'), runs(' Elaborado pelo autor (2026).', 'TcL'))
if 'draw:name="apendiceA"' not in x:
    x = x[:a] + h + fig + x[b:]
else:
    x = x[:a] + h + x[b:]
if img_name not in manifest:
    manifest = manifest.replace('</manifest:manifest>', '<manifest:file-entry manifest:full-path="%s" manifest:media-type="image/png"/></manifest:manifest>' % img_name)

figs, quads = captions('Figura'), captions('Quadro')
replace_entries('LISTA DE ILUSTRAÇÕES (FIGURAS)', 'LISTA DE QUADROS', figs, lista_entry('P186'))
replace_entries('LISTA DE QUADROS', 'LISTA DE ABREVIATURAS E SIGLAS', quads, lista_entry('P261'))

# siglas presentes no texto do corpo (do sumário em diante)
corpo = plain(re.sub(r'</text:(p|h)>', r' </text:\1>', x[body_start():]))
usadas = [s for s in sorted(SIGLAS, key=lambda s: s.replace(' ', '')) if re.search(r'(?<![A-Za-z0-9])%s(?:s|\d+)?(?![A-Za-z0-9])' % re.escape(s), corpo)]

def sigla_entry(s):
    pt, en = SIGLAS[s]
    txt = '%s – %s' % (s, pt) + (' (*%s*)' % en if en else '')
    return '<text:p text:style-name="Normal">%s</text:p>' % runs(txt)

replace_entries('LISTA DE ABREVIATURAS E SIGLAS', 'SUMÁRIO', usadas, sigla_entry)

# ---------- sumário (corpo do índice) ----------
styles = dict(re.findall(r'<style:style style:name="([^"]+)" style:parent-style-name="(Heading\d)"', x))
heads = []
n = [0, 0, 0]
started = False
for m in re.finditer(r'<text:(p|h)\b([^>]*?)(?<!/)>(.*?)</text:\1>', x[body_start():], re.S):
    st = re.search(r'text:style-name="([^"]+)"', m.group(2))
    st = st.group(1) if st else ''
    par = styles.get(st)
    t = plain(m.group(3)).strip()
    if not t:
        continue
    if m.group(1) == 'h' and t in ('REFERÊNCIAS',) or t.startswith('APÊNDICE'):
        heads.append((1, t)); continue
    if par not in ('Heading1', 'Heading2', 'Heading3'):
        continue
    lvl = int(par[-1])
    if lvl == 1 and t == 'INTRODUÇÃO':
        started = True
    if not started:
        continue
    n[lvl - 1] += 1
    for k in range(lvl, 3):
        n[k] = 0
    num = '.'.join(str(v) for v in n[:lvl])
    heads.append((lvl, '%s %s' % (num, t)))

toc = x[x.find('<text:index-body>'):body_start()]
lvl_style = {}
for m in re.finditer(r'<text:p text:style-name="([^"]+)"><text:span text:style-name="([^"]+)">([0-9.]+) ', toc):
    lvl = m.group(3).count('.') + 1 if m.group(3).count('.') else 1
    lvl_style.setdefault(min(lvl, 3), m.group(1))
body = ''.join('<text:p text:style-name="%s">%s<text:span text:style-name="TcT"><text:tab/></text:span></text:p>'
               % (lvl_style.get(l, lvl_style[1]), runs(t)) for l, t in heads)
i = x.find('<text:index-body>')
j = x.find('</text:index-body>', i)
title = re.match(r'<text:index-body>(<text:index-title\b.*?</text:index-title>)?', x[i:j], re.S).group(0)
x = x[:i] + title + body + x[j:]

ET.fromstring(x.encode('utf-8'))

# ---------- citações × referências (só relatório) ----------
ref_start = x.find('>REFERÊNCIAS</text:span></text:h>')
refs_txt = [plain(p) for p in re.findall(r'<text:p\b[^>]*>.*?</text:p>', x[ref_start:x.find('APÊNDICE A', ref_start)], re.S)]
refs_txt = [r for r in refs_txt if r.strip()]
texto = plain(x[x.find('>INTRODUÇÃO<', body_start()):ref_start])
for r in refs_txt:
    autor = re.split(r'[.,;]', r)[0].strip()
    chave = autor.split()[0].capitalize() if autor.isupper() else autor.split()[0]
    if chave.lower() not in texto.lower():
        print('referência sem citação aparente:', r[:90])

zout = zipfile.ZipFile(dst, 'w')
for item in zin.infolist():
    data = {'content.xml': x.encode('utf-8'), 'META-INF/manifest.xml': manifest.encode('utf-8')}.get(item.filename) or zin.read(item.filename)
    zout.writestr(item, data, compress_type=zipfile.ZIP_STORED if item.filename == 'mimetype' else zipfile.ZIP_DEFLATED)
if img_name not in zin.namelist():
    zout.writestr(img_name, open(APX_IMG, 'rb').read(), compress_type=zipfile.ZIP_STORED)
zout.close()
print('figuras: %d, quadros: %d, siglas: %d, títulos no sumário: %d' % (len(figs), len(quads), len(usadas), len(heads)))
