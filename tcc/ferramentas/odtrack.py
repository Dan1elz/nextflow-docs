"""Aplica alterações controladas (ODF tracked changes) num content.xml de ODT.

Uso: python3 -I odtrack.py <entrada.odt> <saida.odt> <ops.py>
ops.py define OPS = [dict(...)] com:
  replace:     {'para': chave, 'old': texto, 'new': texto, 'span': 'T123' opcional}
  append:      {'para': chave, 'append': texto}
  append_item: {'para': chave, 'item': [(estilo_span, texto), ...]}
chave = trecho único do texto do parágrafo, ou '@P123' (nome do estilo do parágrafo).
"""
import re, sys, zipfile, runpy
import xml.etree.ElementTree as ET

AUTHOR = 'Claude (revisão TCC)'
DATE = '2026-11-09T15:00:00'

src, dst, opsfile = sys.argv[1:4]
OPS = runpy.run_path(opsfile)['OPS']

zin = zipfile.ZipFile(src)
x = zin.read('content.xml').decode('utf-8')

regions = []
counter = [0]

def new_id():
    counter[0] += 1
    return 'ctc%d' % counter[0]

def info():
    return ('<office:change-info><dc:creator>%s</dc:creator><dc:date>%s</dc:date>'
            '</office:change-info>' % (AUTHOR, DATE))

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

HL = 'TccNovo'

def hl(s):
    return '<text:span text:style-name="%s">%s</text:span>' % (HL, s)

def text_xml(s):
    s = esc(s)
    s = re.sub(r'  +', lambda m: ' ' + '<text:s text:c="%d"/>' % (len(m.group(0)) - 1), s)
    if s.startswith(' '):
        s = '<text:s/>' + s[1:]
    if s.endswith(' '):
        s = s[:-1] + '<text:s/>'
    return s

def ins_markup(new):
    cid = new_id()
    regions.append('<text:changed-region xml:id="%s" text:id="%s"><text:insertion>%s</text:insertion>'
                   '</text:changed-region>' % (cid, cid, info()))
    return ('<text:change-start text:change-id="%s"/>' % cid, '<text:change-end text:change-id="%s"/>' % cid)

def del_markup(raw):
    cid = new_id()
    regions.append('<text:changed-region xml:id="%s" text:id="%s"><text:deletion>%s<text:p>%s</text:p>'
                   '</text:deletion></text:changed-region>' % (cid, cid, info(), raw))
    return '<text:change text:change-id="%s"/>' % cid

PARA_RE = re.compile(r'<text:(p|h)\b[^>]*?(?:/>|>.*?</text:\1>)', re.S)

def plain(p):
    p = re.sub(r'<text:s(?: text:c="(\d+)")?/>', lambda m: ' ' * int(m.group(1) or 1), p)
    p = re.sub(r'<text:tab/>', '\t', p)
    return re.sub(r'<[^>]+>', '', p).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')

def find_para(key):
    hits = []
    for m in PARA_RE.finditer(x):
        p = m.group(0)
        if key.startswith('@'):
            if re.match(r'<text:(p|h) text:style-name="%s"' % re.escape(key[1:]), p):
                hits.append(m)
        elif key in plain(p):
            hits.append(m)
    if len(hits) != 1:
        raise SystemExit('parágrafo %r: %d ocorrências' % (key, len(hits)))
    return hits[0].start(), hits[0].end()

def old_regex(old):
    parts = []
    for ch in old:
        if ch == ' ':
            parts.append(r'(?: |<text:s/>)')
        else:
            parts.append(re.escape(esc(ch)))
    return re.compile(''.join(parts))

for op in OPS:
    a, b = find_para(op['para'])
    p = x[a:b]
    if 'old' in op:
        lo, hi = 0, len(p)
        if op.get('span'):
            opens = list(re.finditer(r'<text:span text:style-name="%s">' % op['span'], p))
            if len(opens) != 1:
                raise SystemExit('span %s em %r: %d' % (op['span'], op['para'], len(opens)))
            lo = opens[0].end()
            depth, pos = 1, lo
            for t in re.finditer(r'<text:span\b[^>]*?(/?)>|</text:span>', p[lo:]):
                if t.group(0) == '</text:span>':
                    depth -= 1
                elif not t.group(1):
                    depth += 1
                if depth == 0:
                    hi = lo + t.start()
                    break
        ms = list(old_regex(op['old']).finditer(p, lo, hi))
        if len(ms) != 1:
            raise SystemExit('trecho %r em %r: %d ocorrências' % (op['old'], op['para'], len(ms)))
        m = ms[0]
        rep = del_markup(m.group(0))
        if op['new']:
            s, e = ins_markup(op['new'])
            rep += s + hl(text_xml(op['new'])) + e
        p = p[:m.start()] + rep + p[m.end():]
        x = x[:a] + p + x[b:]
    elif 'append' in op:
        i = p.rfind('</text:span>')
        if i < 0:
            i = p.rfind('</text:p>')
        s, e = ins_markup(op['append'])
        p = p[:i] + s + hl(text_xml(op['append'])) + e + p[i:]
        x = x[:a] + p + x[b:]
    elif 'item' in op:
        style = re.match(r'<text:p text:style-name="([^"]+)"', p).group(1)
        li_end = x.find('</text:list-item>', b)
        assert li_end > 0 and x.find('<text:list-item', b) == -1 or x.find('<text:list-item', b) > li_end
        s, e = ins_markup('item')
        spans = ''.join('<text:span text:style-name="%s">%s</text:span>' % (st, hl(text_xml(t))) for st, t in op['item'])
        spans = spans[:-len('</text:span>')] + e + '</text:span>'
        new_item = '<text:list-item><text:p text:style-name="%s">%s</text:p></text:list-item>' % (style, spans)
        # marca o início da inserção no fim do parágrafo anterior
        close = b - len('</text:p>')
        assert x[close:b] == '</text:p>'
        x = x[:close] + s + x[close:li_end + len('</text:list-item>')] + new_item + x[li_end + len('</text:list-item>'):]
    print('ok:', op.get('old') or op.get('append') or op['item'][0][1])

# estilo do destaque verde (sai com limpar_destaque.py)
if 'style:name="%s"' % HL not in x:
    x = x.replace('<office:automatic-styles>', '<office:automatic-styles><style:style style:name="%s" style:family="text">'
                  '<style:text-properties fo:background-color="#c6efce"/></style:style>' % HL, 1)

# insere o bloco de alterações logo depois de <office:text ...>
m = re.search(r'<office:text\b[^>]*>', x)
block = '<text:tracked-changes text:track-changes="false">%s</text:tracked-changes>' % ''.join(regions)
x = x[:m.end()] + block + x[m.end():]
ET.fromstring(x.encode('utf-8'))  # falha se o XML ficou malformado

zout = zipfile.ZipFile(dst, 'w')
for item in zin.infolist():
    data = x.encode('utf-8') if item.filename == 'content.xml' else zin.read(item.filename)
    if item.filename == 'mimetype':
        zout.writestr(item, data, compress_type=zipfile.ZIP_STORED)
    else:
        zout.writestr(item, data, compress_type=zipfile.ZIP_DEFLATED)
zout.close()
print('alterações:', len(regions))
