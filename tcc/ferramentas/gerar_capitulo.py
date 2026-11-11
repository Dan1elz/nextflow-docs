"""Substitui um capítulo inteiro do ODT pelo conteúdo de um arquivo-fonte (ex.: cap4.py).

Uso (da pasta tcc/ferramentas): python3 -I gerar_capitulo.py <entrada.odt> <saida.odt> cap4.py

- Mantém o título do capítulo (Heading 1) e troca tudo até o título do capítulo seguinte.
- Todo texto novo leva o fundo verde TccNovo (sai com limpar_destaque.py).
- Figuras e quadros são numerados na ordem; {fig:x}/{qd:x} viram "Figura N"/"Quadro N".
- Imagens entram em media/ e as que deixam de ser usadas saem do arquivo.
"""
import os, re, sys, struct, zipfile, runpy

HERE = os.path.dirname(os.path.abspath(__file__))
src, dst, fonte = sys.argv[1:4]
CAP = runpy.run_path(os.path.join(HERE, fonte))
ESQ = os.path.join(HERE, '../../docs/architecture/diagrams/uml/der/esquema')

TITULO_ATUAL = CAP.get('TITULO', 'DESENVOLVIMENTO')
TITULO_SEGUINTE = CAP.get('TITULO_SEGUINTE', 'RESULTADOS E DISCUSSÃO')
HL = 'TccNovo'
FONTE_TXT = 'Elaborado pelo autor (2026).'

zin = zipfile.ZipFile(src)
x = zin.read('content.xml').decode('utf-8')
manifest = zin.read('META-INF/manifest.xml').decode('utf-8')

# ---------- estilos ----------
LANG = 'fo:language="pt" fo:country="BR"'
SZ10 = 'fo:font-size="10pt" style:font-size-asian="10pt" style:font-size-complex="10pt"'
BOLD = 'fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold"'
ITAL = 'fo:font-style="italic" style:font-style-asian="italic" style:font-style-complex="italic"'
STYLES = {
    'TccNovo': '<style:style style:name="TccNovo" style:family="text"><style:text-properties fo:background-color="#c6efce"/></style:style>',
    'TcCorpo': '<style:style style:name="TcCorpo" style:parent-style-name="Normal" style:family="paragraph"><style:paragraph-properties fo:text-indent="0.4923in"/></style:style>',
    'TcAlinea': '<style:style style:name="TcAlinea" style:parent-style-name="Normal" style:family="paragraph"/>',
    'TcT': '<style:style style:name="TcT" style:family="text"><style:text-properties %s/></style:style>' % LANG,
    'TcI': '<style:style style:name="TcI" style:family="text"><style:text-properties %s %s/></style:style>' % (ITAL, LANG),
    'TcB': '<style:style style:name="TcB" style:family="text"><style:text-properties %s %s/></style:style>' % (BOLD, LANG),
    'TcL': '<style:style style:name="TcL" style:family="text"><style:text-properties %s %s/></style:style>' % (SZ10, LANG),
    'TcLI': '<style:style style:name="TcLI" style:family="text"><style:text-properties %s %s %s/></style:style>' % (SZ10, ITAL, LANG),
    'TcLB': '<style:style style:name="TcLB" style:family="text"><style:text-properties %s %s %s/></style:style>' % (SZ10, BOLD, LANG),
    'TcFig': '<style:style style:name="TcFig" style:family="graphic"><style:graphic-properties style:wrap="none" '
             'style:vertical-pos="top" style:vertical-rel="baseline" style:horizontal-pos="center" '
             'style:horizontal-rel="paragraph"/></style:style>',
}
extra_styles = []

# ---------- texto ----------
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

FIG, QD = {}, {}

def refs(s):
    def r(m):
        kind, key = m.group(1), m.group(2)
        n = (FIG if kind == 'fig' else QD)[key]
        return ('Figura %d' if kind == 'fig' else 'Quadro %d') % n
    return re.sub(r'\{(fig|qd):([a-z0-9]+)\}', r, s)

def runs(s, small=False):
    """*itálico* e **negrito** em spans; cada pedaço com o fundo verde por dentro."""
    s = refs(s)
    out = []
    for part in re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)', s):
        if not part:
            continue
        if part.startswith('**'):
            st, t = ('TcLB' if small else 'TcB'), part[2:-2]
        elif part.startswith('*'):
            st, t = ('TcLI' if small else 'TcI'), part[1:-1]
        else:
            st, t = ('TcL' if small else 'TcT'), part
        out.append('<text:span text:style-name="%s"><text:span text:style-name="%s">%s</text:span></text:span>'
                   % (st, HL, text_xml(t)))
    return ''.join(out)

def para(style, s, small=False):
    return '<text:p text:style-name="%s">%s</text:p>' % (style, runs(s, small))

def heading(level, s):
    style = {2: 'P875', 3: 'P1130', 4: 'P1550'}[level]
    inner = '<text:p text:style-name="%s"><text:span text:style-name="%s">%s</text:span></text:p>' % (style, HL, text_xml(s))
    for _ in range(level):
        inner = '<text:list><text:list-item>%s</text:list-item></text:list>' % inner
    # o nível de fora é a lista de títulos do documento
    inner = inner[len('<text:list>'):]
    return '<text:list text:style-name="LFO13" text:continue-numbering="true">' + inner

def alineas(items):
    out = []
    for i, (rot, txt) in enumerate(items):
        start = ' text:start-value="1"' if i == 0 else ''
        out.append('<text:list-item%s><text:p text:style-name="TcAlinea">%s%s</text:p></text:list-item>'
                   % (start, runs('**%s:**' % rot), runs(' ' + txt)))
    return '<text:list text:style-name="LFO16">%s</text:list>' % ''.join(out)

def caption(kind, n, legenda):
    return ('<text:p text:style-name="P916">%s</text:p>' % runs('%s %d – %s' % (kind, n, legenda), small=True))

def fonte():
    return '<text:p text:style-name="P1138">%s%s</text:p>' % (runs('**Fonte:**', small=True), runs(' ' + FONTE_TXT, small=True))

# ---------- figuras ----------
images = {}  # caminho de origem -> nome no zip

def png_size(path):
    with open(path, 'rb') as f:
        d = f.read(24)
    return struct.unpack('>II', d[16:24])

def figure(key, legenda, path, maxw):
    full = os.path.normpath(os.path.join(HERE, path))
    w, h = png_size(full)
    width = min(maxw, 6.3)
    height = width * h / w
    if height > 8.2:
        height = 8.2
        width = height * w / h
    name = 'media/tcc_%s_%s' % (os.path.basename(os.path.dirname(full)), os.path.basename(full))
    images[full] = name
    frame = ('<draw:frame draw:style-name="TcFig" draw:name="%s" text:anchor-type="as-char" svg:width="%.3fin" '
             'svg:height="%.3fin" draw:z-index="0"><draw:image xlink:href="%s" xlink:type="simple" xlink:show="embed" '
             'xlink:actuate="onLoad"/></draw:frame>') % (key, width, height, name)
    return caption('Figura', FIG[key], legenda) + '<text:p text:style-name="P1137">%s</text:p>' % frame + fonte()

# ---------- quadros ----------
tab_n = [0]
TAB = 'TcTab%s_' % CAP.get('NUMERO', '4')

def cell(spec, ncols_left):
    span = 1
    m = re.match(r'(H)?S(\d+):', spec)
    header = spec.startswith('H:')
    if m:
        header, span = bool(m.group(1)), int(m.group(2))
        spec = spec[m.end():]
    elif header:
        spec = spec[2:]
    cstyle = 'TableCell925' if header else 'TableCell935'
    pstyle = 'P926' if header else 'P939'
    body = runs('**%s**' % spec, small=True) if header and spec else runs(spec, small=True) if spec else ''
    attr = ' table:number-columns-spanned="%d"' % span if span > 1 else ''
    xml = '<table:table-cell table:style-name="%s" office:value-type="string"%s><text:p text:style-name="%s">%s</text:p></table:table-cell>' % (
        cstyle, attr, pstyle, body)
    xml += '<table:covered-table-cell/>' * (span - 1)
    return xml, span

def table(widths, rows):
    tab_n[0] += 1
    t = '%s%d' % (TAB, tab_n[0])
    extra_styles.append('<style:style style:name="%s" style:family="table"><style:table-properties style:width="%.4fin" '
                        'fo:margin-left="0in" table:align="left"/></style:style>' % (t, sum(widths)))
    cols = ''
    for i, w in enumerate(widths):
        extra_styles.append('<style:style style:name="%sC%d" style:family="table-column"><style:table-column-properties '
                            'style:column-width="%.4fin" style:use-optimal-column-width="false"/></style:style>' % (t, i, w))
        cols += '<table:table-column table:style-name="%sC%d"/>' % (t, i)
    head, body = [], []
    for r in rows:
        cells = ''.join(cell(c, 0)[0] for c in r)
        is_head = all(c.startswith(('H:', 'HS')) for c in r)
        row = '<table:table-row%s>%s</table:table-row>' % (' table:style-name="TableRow924"' if is_head else '', cells)
        (head if is_head and not body else body).append(row)
    hx = '<table:table-header-rows>%s</table:table-header-rows>' % ''.join(head) if head else ''
    return '<table:table table:name="%s" table:style-name="%s"><table:table-columns>%s</table:table-columns>%s%s</table:table>' % (
        t, t, cols, hx, ''.join(body))

def quadro(key, legenda, widths, rows):
    return caption('Quadro', QD[key], legenda) + table(widths, rows) + fonte()

# ---------- dicionário de dados ----------
CLASSE = {'uuid': 'UUID', 'character varying': 'VARCHAR', 'numeric': 'NUMERIC', 'smallint': 'SMALLINT',
          'integer': 'INTEGER', 'boolean': 'BOOLEAN', 'date': 'DATE', 'timestamp with time zone': 'TIMESTAMPTZ'}

def dd_rows(tabela, desc):
    cols = [l.split('|') for l in open(os.path.join(ESQ, 'colunas.txt'), encoding='utf-8') if l.startswith(tabela + '|')]
    keys = [l.strip().split('|') for l in open(os.path.join(ESQ, 'chaves.txt'), encoding='utf-8') if l.startswith(tabela + '|')]
    pk = {k[1] for k in keys if k[3] == 'PRIMARY KEY'}
    fk = {k[1] for k in keys if k[3] == 'FOREIGN KEY'}
    un = set()
    for l in open(os.path.join(ESQ, 'indices-unicos.txt'), encoding='utf-8'):
        m = re.search(r'ON public\.(\w+) USING btree \((\w+)\)', l)
        if m and m.group(1) == tabela and ' pk_' not in l:
            un.add(m.group(2))
    rows = [['HS5:Tabela: %s' % tabela], ['H:Atributo', 'H:Classe', 'H:Domínio', 'H:Tamanho', 'H:Descrição']]
    faltando = [c for c in desc if c not in {c[1] for c in cols}]
    if faltando:
        raise SystemExit('colunas inexistentes em %s: %s' % (tabela, faltando))
    for c in sorted(cols, key=lambda c: int(c[5])):
        nome, tipo, nulo, tam, prec, esc_ = c[1], c[2], c[3], c[4], c[6], c[7].strip()
        if nome not in desc:
            continue
        dom = [d for d, ok in (('PK', nome in pk), ('FK', nome in fk), ('NN', nulo == 'NO'), ('UN', nome in un)) if ok]
        if tipo == 'character varying':
            tamanho = tam
        elif tipo == 'numeric':
            tamanho = '%s,%s' % (prec, esc_)
        else:
            tamanho = '-'
        rows.append([nome, CLASSE[tipo], ', '.join(dom) or '-', tamanho, desc[nome]])
    return rows

# ---------- montagem ----------
blocos = CAP['BLOCOS']
nf, nq = CAP.get('FIG_INICIO', 0), CAP.get('QD_INICIO', 0)
for b in blocos:
    if b[0] == 'fig':
        nf += 1; FIG[b[1]] = nf
    elif b[0] in ('quadro', 'dd'):
        nq += 1; QD[b[1]] = nq

out = [para('TcCorpo', CAP['INTRO'])]
for b in blocos:
    k = b[0]
    if k == 'h2':
        out.append(heading(2, b[1]))
    elif k == 'h3':
        out.append(heading(3, b[1]))
    elif k == 'p':
        out.append(para('TcCorpo', b[1]))
    elif k == 'alineas':
        out.append(alineas(b[1]))
    elif k == 'fig':
        out.append(figure(b[1], b[2], b[3], b[4]))
    elif k == 'quadro':
        out.append(quadro(b[1], b[2], b[3], b[4]))
    elif k == 'dd':
        out.append(quadro(b[1], 'Dicionário de dados da tabela %s.' % b[2], [1.35, 0.95, 0.85, 0.75, 2.4], dd_rows(b[2], b[3])))
    else:
        raise SystemExit('bloco desconhecido: %r' % (k,))
novo = ''.join(out)

# região do capítulo: depois da lista do título atual até a lista do título seguinte
m = re.search(r'<text:list [^>]*><text:list-item><text:p text:style-name="[^"]+">(?:<text:bookmark-[^>]*/>)*%s</text:p></text:list-item></text:list>' % re.escape(TITULO_ATUAL), x)
if not m:
    raise SystemExit('título do capítulo não encontrado')
a = m.end()
j = x.find('%s</text:p>' % TITULO_SEGUINTE, a)
if j >= 0:
    b = x.rfind('<text:list ', a, j)
else:
    # título seguinte fora de lista (ex.: REFERÊNCIAS em <text:h>): para antes dele e dos parágrafos vazios que o precedem
    j = x.find('>%s</text:span></text:h>' % TITULO_SEGUINTE, a)
    if j < 0:
        raise SystemExit('título seguinte não encontrado')
    b = x.rfind('<text:h ', a, j)
    while True:
        mm = re.search(r'<text:p text:style-name="[^"]+"/>$', x[a:b])
        if not mm:
            break
        b = a + mm.start()
old = x[a:b]
if 'text:change' in old:
    raise SystemExit('o capítulo tem alterações controladas pendentes; aceite-as antes de regerar')
x = x[:a] + novo + x[b:]

# referências novas
for depois_de, ref in CAP.get('REFERENCIAS', []):
    if refs(ref).split('.')[0] in re.sub(r'<[^>]+>', '', x[x.find('REFERÊNCIAS'):]):
        continue
    i = x.find(depois_de, x.find('REFERÊNCIAS'))
    e = x.find('</text:p>', i) + len('</text:p>')
    st = re.findall(r'<text:p text:style-name="([^"]+)"', x[:i])[-1]
    x = x[:e] + '<text:p text:style-name="%s">%s</text:p>' % (st, runs(ref)) + x[e:]

# estilos automáticos
add = ''.join(v for k, v in STYLES.items() if 'style:name="%s"' % k not in x) + ''.join(extra_styles)
x = re.sub(r'<style:style style:name="%s\d+(C\d+)?"[^>]*>.*?</style:style>' % TAB, '', x)  # regerar sem duplicar
x = x.replace('<office:automatic-styles>', '<office:automatic-styles>' + add, 1)

import xml.etree.ElementTree as ET
ET.fromstring(x.encode('utf-8'))

# imagens: novas entram, as que ninguém usa saem
used = set(re.findall(r'xlink:href="(media/[^"]+)"', x))
entries = []
for item in zin.infolist():
    if item.filename.startswith('media/') and item.filename not in used:
        continue
    if item.filename in images.values():
        continue
    entries.append(item)
mf = re.sub(r'<manifest:file-entry manifest:full-path="(media/[^"]+)"[^>]*/>',
            lambda mm: mm.group(0) if mm.group(1) in used else '', manifest)
for full, name in images.items():
    mf = mf.replace('</manifest:manifest>', '<manifest:file-entry manifest:full-path="%s" manifest:media-type="image/png"/></manifest:manifest>' % name)

zout = zipfile.ZipFile(dst, 'w')
for item in entries:
    if item.filename == 'content.xml':
        data = x.encode('utf-8')
    elif item.filename == 'META-INF/manifest.xml':
        data = mf.encode('utf-8')
    else:
        data = zin.read(item.filename)
    zout.writestr(item, data, compress_type=zipfile.ZIP_STORED if item.filename == 'mimetype' else zipfile.ZIP_DEFLATED)
for full, name in images.items():
    zout.writestr(name, open(full, 'rb').read(), compress_type=zipfile.ZIP_STORED)
zout.close()
print('figuras: %d, quadros: %d, imagens novas: %d, mídia removida: %d' % (
    nf, nq, len(images), sum(1 for i in zin.infolist() if i.filename.startswith('media/') and i.filename not in used)))
