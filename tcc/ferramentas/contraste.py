"""Contraste WCAG 2.2 dos tokens OKLCH do front. Uso: python3 -I contraste.py index.css"""
import re, math, sys
css = open(sys.argv[1]).read()
def block(sel):
    i = css.index(sel + ' {'); j = css.index('}', i)
    return dict(re.findall(r'--([a-z-]+):\s*([^;]+);', css[i:j]))
def parse(v):
    m = re.match(r'oklch\(([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*/\s*([\d.]+)%)?\)', v.strip())
    l, c, h, a = m.groups(); return float(l), float(c), float(h), (float(a) / 100 if a else 1.0)
def lin(l, c, h):
    a = c * math.cos(math.radians(h)); b = c * math.sin(math.radians(h))
    l_ = l + 0.3963377774*a + 0.2158037573*b; m_ = l - 0.1055613458*a - 0.0638541728*b; s_ = l - 0.0894841775*a - 1.2914855480*b
    l3, m3, s3 = l_**3, m_**3, s_**3
    return [min(1, max(0, x)) for x in (4.0767416621*l3 - 3.3077115913*m3 + 0.2309699292*s3,
                                        -1.2684380046*l3 + 2.6097574011*m3 - 0.3413193965*s3,
                                        -0.0041960863*l3 - 0.7034186147*m3 + 1.7076147010*s3)]
enc = lambda x: 12.92*x if x <= 0.0031308 else 1.055*x**(1/2.4) - 0.055
dec = lambda x: x/12.92 if x <= 0.04045 else ((x + 0.055)/1.055)**2.4
def srgb(v, bg=None):
    l, c, h, a = parse(v); rgb = [enc(x) for x in lin(l, c, h)]
    return [a*x + (1-a)*y for x, y in zip(rgb, bg)] if a < 1 else rgb
lum = lambda rgb: sum(k*dec(x) for k, x in zip((0.2126, 0.7152, 0.0722), rgb))
ratio = lambda f, b: (max(lum(f), lum(b)) + 0.05) / (min(lum(f), lum(b)) + 0.05)
PARES = [('Texto principal sobre o fundo', 'foreground', 'background', 4.5),
         ('Texto em cartões', 'card-foreground', 'card', 4.5),
         ('Texto secundário sobre o fundo', 'muted-foreground', 'background', 4.5),
         ('Texto secundário em cartões', 'muted-foreground', 'card', 4.5),
         ('Texto do botão principal', 'primary-foreground', 'primary', 4.5),
         ('Destaque e links sobre o fundo', 'primary', 'background', 4.5),
         ('Destaque e links em cartões', 'primary', 'card', 4.5),
         ('Mensagem de erro sobre o fundo', 'destructive', 'background', 4.5),
         ('Mensagem de erro em cartões', 'destructive', 'card', 4.5),
         ('Texto do botão de exclusão', 'destructive-foreground', 'destructive', 4.5),
         ('Item ativo do menu lateral', 'sidebar-primary-foreground', 'sidebar-primary', 4.5),
         ('Texto do menu lateral', 'sidebar-foreground', 'sidebar', 4.5),
         ('Borda dos campos (cartão)', 'input', 'card', 3.0),
         ('Borda dos campos (fundo)', 'input', 'background', 3.0),
         ('Anel de foco (cartão)', 'ring', 'card', 3.0),
         ('Anel de foco (fundo)', 'ring', 'background', 3.0)]
for nome, sel in (('claro', ':root'), ('escuro', '.dark')):
    T = block(sel); print('==', nome)
    for rot, f, b, mn in PARES:
        bg = srgb(T[b]); r = ratio(srgb(T[f], bg), bg)
        print(f'{rot:34s} {r:5.2f}:1 {"ok" if r >= mn else "ABAIXO"} (mín {mn})')
