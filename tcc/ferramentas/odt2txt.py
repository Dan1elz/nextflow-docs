import sys, zipfile, xml.etree.ElementTree as ET

NS = {
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
}
T = '{%s}' % NS['text']
TB = '{%s}' % NS['table']
D = '{%s}' % NS['draw']
XL = '{%s}' % NS['xlink']

def inline(el):
    out = [el.text or '']
    for c in el:
        tag = c.tag
        if tag == T + 's':
            out.append(' ' * int(c.get(T + 'c', '1')))
        elif tag == T + 'tab':
            out.append('\t')
        elif tag == T + 'line-break':
            out.append('\n')
        elif tag == T + 'note':
            body = c.find(T + 'note-body')
            txt = ' '.join(inline(p) for p in body.iter(T + 'p')) if body is not None else ''
            out.append(' [NOTA: %s]' % txt)
        elif tag == D + 'frame':
            img = c.find(D + 'image')
            if img is not None:
                out.append(' [IMG %s]' % img.get(XL + 'href'))
            tb = c.find(D + 'text-box')
            if tb is not None:
                out.append(' '.join(inline(p) for p in tb.iter(T + 'p')))
        elif tag in (T + 'soft-page-break', T + 'bookmark', T + 'bookmark-start', T + 'bookmark-end'):
            pass
        else:
            out.append(inline(c))
        out.append(c.tail or '')
    return ''.join(out)

lines = []
def walk(el, depth=0):
    for c in el:
        tag = c.tag
        if tag == T + 'h':
            lvl = c.get(T + 'outline-level', '1')
            lines.append('\n' + '#' * int(lvl) + ' ' + inline(c).strip())
        elif tag == T + 'p':
            s = inline(c).strip()
            if s:
                lines.append(s)
        elif tag == T + 'list':
            for item in c.iter(T + 'list-item'):
                for p in item.findall(T + 'p'):
                    s = inline(p).strip()
                    if s:
                        lines.append('- ' + s)
                for h in item.findall(T + 'h'):
                    lvl = h.get(T + 'outline-level', '1')
                    lines.append('\n' + '#' * int(lvl) + ' ' + inline(h).strip())
        elif tag == TB + 'table':
            lines.append('[TABELA]')
            for row in c.iter(TB + 'table-row'):
                cells = []
                for cell in row.findall(TB + 'table-cell'):
                    cells.append(' / '.join(inline(p).strip() for p in cell.iter(T + 'p')))
                lines.append('| ' + ' | '.join(cells) + ' |')
            lines.append('[/TABELA]')
        elif tag in (T + 'section', T + 'table-of-content', T + 'index-body'):
            if tag == T + 'table-of-content':
                lines.append('[SUMARIO omitido]')
                continue
            walk(c, depth + 1)

z = zipfile.ZipFile(sys.argv[1])
root = ET.fromstring(z.read('content.xml'))
body = root.find('office:body/office:text', NS)
walk(body)
open(sys.argv[2], 'w').write('\n'.join(lines))
