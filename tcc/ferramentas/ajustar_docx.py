"""Ajustes no DOCX final do TCC (depois que o Daniel passou a trabalhar no .docx).

Uso: python3 -I ajustar_docx.py <entrada.docx> <saida.docx>

1. Tira o fundo verde (sombreamento C6EFCE) de todo o documento.
2. Remove o preenchimento em degradê, a borda azul e a sombra que a conversão ODT -> DOCX pôs nas imagens.
3. Transforma as legendas "Figura N – ..." e "Quadro N – ..." em legendas do Word (estilo Legenda + campo SEQ).
4. Troca as listas de figuras e de quadros digitadas pelo índice de ilustrações do Word (campo TOC \\c), com página.
5. Marca o documento para atualizar os campos ao abrir (números de página das listas e do sumário).
"""
import re, sys, zipfile

src, dst = sys.argv[1:3]
zin = zipfile.ZipFile(src)
doc = zin.read('word/document.xml').decode('utf-8')
styles = zin.read('word/styles.xml').decode('utf-8')
settings = zin.read('word/settings.xml').decode('utf-8')

# 1. fundo verde
#    Só nos pré e pós-textuais: o verde fica nos capítulos 1 a 6 (o grupo revisa por ele; Daniel, 09/11).
VERDE = '<w:shd w:val="clear" w:color="auto" w:fill="C6EFCE"/>'
PARA = re.compile(r'<w:p\b[^>]*>(?:(?!</w:p>).)*</w:p>', re.S)

def inicio_titulo(txt):
    for m in PARA.finditer(doc):
        p = m.group(0)
        if re.search(r'<w:pStyle w:val="Ttulo\d"/>', p) and ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', p)).strip() == txt:
            return m.start()
    raise SystemExit('título %s não encontrado' % txt)

ini_txt, fim_txt = inicio_titulo('INTRODUÇÃO'), inicio_titulo('REFERÊNCIAS')
fora = lambda s: re.sub(re.escape(VERDE), '', s, flags=re.I).replace('<w:rPr></w:rPr>', '')
antes = len(re.findall(r'w:fill="C6EFCE"', doc[:ini_txt] + doc[fim_txt:], re.I))
doc = fora(doc[:ini_txt]) + doc[ini_txt:fim_txt] + fora(doc[fim_txt:])

# 1b. parágrafo dos logos da capa estava com estilo de título e entrava no sumário
m = PARA.search(doc)
if '<w:drawing' in m.group(0) and '<w:pStyle w:val="Ttulo2"/>' in m.group(0):
    doc = doc[:m.start()] + m.group(0).replace('<w:pPr><w:pStyle w:val="Ttulo2"/></w:pPr>', '<w:pPr><w:keepNext/></w:pPr>', 1) + doc[m.end():]

# 2. imagens: só geometria, sem preenchimento, linha ou sombra
def limpa_sppr(m):
    sp = m.group(0)
    sp = re.sub(r'<a:gradFill>.*?</a:gradFill>|<a:solidFill>.*?</a:solidFill>(?=<a:ln)', '', sp, flags=re.S)
    sp = re.sub(r'<a:ln\b.*?</a:ln>', '<a:ln><a:noFill/></a:ln>', sp, flags=re.S)
    sp = re.sub(r'<a:effectLst>.*?</a:effectLst>', '', sp, flags=re.S)
    return sp
n_img = len(re.findall(r'<pic:spPr>', doc))
doc = re.sub(r'<pic:spPr>.*?</pic:spPr>', limpa_sppr, doc, flags=re.S)
doc = re.sub(r'<wp:effectExtent [^>]*/>', '<wp:effectExtent l="0" t="0" r="0" b="0"/>', doc)

# estilos Legenda e Índice de ilustrações
if 'w:styleId="Legenda"' not in styles:
    styles = styles.replace('</w:styles>',
        '<w:style w:type="paragraph" w:styleId="Legenda"><w:name w:val="caption"/><w:basedOn w:val="Normal"/>'
        '<w:next w:val="Normal"/><w:uiPriority w:val="35"/><w:unhideWhenUsed/><w:qFormat/>'
        '<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>'
        '<w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style></w:styles>')
if 'w:styleId="ndicedeilustraes"' not in styles:
    styles = styles.replace('</w:styles>',
        '<w:style w:type="paragraph" w:styleId="ndicedeilustraes"><w:name w:val="table of figures"/><w:basedOn w:val="Normal"/>'
        '<w:next w:val="Normal"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/>'
        '<w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9070"/></w:tabs><w:spacing w:after="120" w:line="240" w:lineRule="auto"/>'
        '<w:ind w:firstLine="0"/><w:jc w:val="left"/></w:pPr></w:style></w:styles>')

def texto(p):
    return ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', p))

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# 3. legendas -> estilo Legenda + SEQ (só fora das listas: parágrafo sem tabulação)
cont = {'Figura': 0, 'Quadro': 0}
def legenda(m):
    p = m.group(0)
    t = texto(p)
    mm = re.match(r'^(Figura|Quadro) (\d+) – (.*)$', t)
    if not mm or '<w:tab/>' in p or 'SEQ ' in p:
        return p
    kind, num, resto = mm.groups()
    cont[kind] += 1
    open_tag = re.match(r'<w:p\b[^>]*>', p).group(0)
    shd = VERDE if 'C6EFCE' in p.upper() else ''
    run = lambda s: '<w:r><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (shd, esc(s))
    seq = ('<w:fldSimple w:instr=" SEQ %s \\* ARABIC "><w:r><w:rPr><w:noProof/><w:sz w:val="20"/><w:szCs w:val="20"/>%s</w:rPr>'
           '<w:t>%s</w:t></w:r></w:fldSimple>') % (kind, shd, num)
    return open_tag + '<w:pPr><w:pStyle w:val="Legenda"/></w:pPr>' + run(kind + ' ') + seq + run(' – ' + resto) + '</w:p>'

# localizar as listas para não mexer nelas como legenda
def faixa(titulo, proximo):
    a = doc.find('>%s</w:t>' % titulo)
    a = doc.find('</w:p>', a) + len('</w:p>')
    b = doc.find('>%s</w:t>' % proximo, a)
    b = doc.rfind('<w:p ', a, b)
    return a, b

ini_listas = faixa('LISTA DE ILUSTRAÇÕES (FIGURAS)', 'LISTA DE QUADROS')[0]
fim_siglas = doc.find('>SUMÁRIO</w:t>')
corpo_ini = doc.find('</w:p>', fim_siglas)
doc = doc[:corpo_ini] + PARA.sub(legenda, doc[corpo_ini:])

# 4. listas -> índice de ilustrações (TOC \c), com o resultado atual como cache
def indice(titulo, proximo, rotulo):
    global doc
    a, b = faixa(titulo, proximo)
    seg = doc[a:b]
    paras = PARA.findall(seg)
    entradas = [texto(p) for p in paras if re.match(r'^%s \d+ – ' % rotulo, texto(p))]
    vazios = [p for p in paras if not texto(p).strip() and '<w:drawing' not in p]
    linhas = []
    for i, e in enumerate(entradas):
        ini = ('<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\h \\z \\c "%s" </w:instrText></w:r>'
               '<w:r><w:fldChar w:fldCharType="separate"/></w:r>' % rotulo) if i == 0 else ''
        fim = '<w:r><w:fldChar w:fldCharType="end"/></w:r>' if i == len(entradas) - 1 else ''
        linhas.append('<w:p><w:pPr><w:pStyle w:val="ndicedeilustraes"/></w:pPr>%s<w:r><w:t xml:space="preserve">%s</w:t></w:r>'
                      '<w:r><w:tab/></w:r>%s</w:p>' % (ini, esc(e), fim))
    doc = doc[:a] + ''.join(linhas) + ''.join(vazios) + doc[b:]
    return len(entradas)

nf = indice('LISTA DE ILUSTRAÇÕES (FIGURAS)', 'LISTA DE QUADROS', 'Figura')
nq = indice('LISTA DE QUADROS', 'LISTA DE ABREVIATURAS E SIGLAS', 'Quadro')

# 5. atualizar campos ao abrir
if '<w:updateFields' not in settings:
    settings = re.sub(r'(<w:settings\b[^>]*>)', r'\1<w:updateFields w:val="true"/>', settings, count=1)

import xml.etree.ElementTree as ET
for nome, conteudo in (('document', doc), ('styles', styles), ('settings', settings)):
    ET.fromstring(conteudo.encode('utf-8'))

zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    data = {'word/document.xml': doc, 'word/styles.xml': styles, 'word/settings.xml': settings}.get(it.filename)
    zout.writestr(it, data.encode('utf-8') if data is not None else zin.read(it.filename))
zout.close()
print('verde removido: %d trechos; imagens limpas: %d; legendas: %d figuras e %d quadros; listas: %d figuras e %d quadros'
      % (antes, n_img, cont['Figura'], cont['Quadro'], nf, nq))
