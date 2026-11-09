"""Remove o fundo verde (estilo TccNovo) do ODT, mantendo o texto. Uso: python3 -I limpar_destaque.py arquivo.odt"""
import re, sys, zipfile, shutil, tempfile
path = sys.argv[1]
zin = zipfile.ZipFile(path)
x = zin.read('content.xml').decode('utf-8')
x = re.sub(r'<style:style style:name="TccNovo"[^>]*>.*?</style:style>', '', x, flags=re.S)
x = re.sub(r'<text:span text:style-name="TccNovo">(.*?)</text:span>', r'\1', x, flags=re.S)
tmp = tempfile.mktemp(suffix='.odt')
zout = zipfile.ZipFile(tmp, 'w')
for it in zin.infolist():
    data = x.encode('utf-8') if it.filename == 'content.xml' else zin.read(it.filename)
    zout.writestr(it, data, compress_type=zipfile.ZIP_STORED if it.filename == 'mimetype' else zipfile.ZIP_DEFLATED)
zout.close(); zin.close()
shutil.move(tmp, path)
print('destaque removido')
