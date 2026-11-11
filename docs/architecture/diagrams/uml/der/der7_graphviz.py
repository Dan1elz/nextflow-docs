"""DER 7 (Vendas e promoções) em Graphviz, num formato mais alto que largo para caber legível no PDF do TCC.

O Mermaid põe as sete tabelas de outros módulos numa linha só e não deixa aumentar o texto das ligações; aqui cada
tabela tem a sua linha (rank) e os verbos usam fonte grande. Mesmo conteúdo e cores do der-7-vendas.mmd.

Uso (nesta pasta):
  python3 der7_graphviz.py > der-7-vendas.dot
  docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/data" --entrypoint dot plantuml/plantuml:1.2024.7 \
    -Tpng -Gdpi=200 -o /data/der-7-vendas.png /data/der-7-vendas.dot
"""

CORES = {  # (fundo do cabeçalho, borda), iguais aos classDef do Mermaid
    'venda': ('#E3F2FD', '#1565C0'), 'cadastro': ('#FFF8E1', '#F9A825'), 'previsao': ('#E0F7FA', '#00838F'),
    'produto': ('#EDE7F6', '#5E35B1'), 'estoque': ('#E8F5E9', '#2E7D32'), 'acesso': ('#FCE4EC', '#C2185B'),
}

TABELAS = {
    'orders': ('Venda (orders)', 'venda', [
        ('uuid', 'id', 'PK', ''), ('uuid', 'store_id', 'FK', ''), ('uuid', 'sale_location_id', 'FK', ''),
        ('uuid', 'client_id', 'FK', 'opcional'), ('uuid', 'user_id', 'FK', ''), ('int', 'number', '', ''),
        ('smallint', 'status', '', 'paga ou cancelada'), ('smallint', 'channel', '', 'balcão'),
        ('numeric', 'subtotal', '', ''), ('numeric', 'discount_total', '', ''), ('numeric', 'total', '', ''),
        ('numeric', 'cash_received', '', 'opcional'), ('numeric', 'change', '', 'opcional'),
        ('timestamptz', 'paid_at', '', 'opcional')]),
    'order_items': ('Item da venda (order_items)', 'venda', [
        ('uuid', 'id', 'PK', ''), ('uuid', 'order_id', 'FK', ''), ('uuid', 'variant_id', 'FK', ''),
        ('uuid', 'promotion_id', 'FK', 'opcional'), ('int', 'position', '', ''), ('numeric', 'quantity', '', ''),
        ('numeric', 'list_price', '', ''), ('numeric', 'unit_price', '', ''), ('numeric', 'discount', '', ''),
        ('numeric', 'line_total', '', ''), ('numeric', 'unit_cost', '', 'opcional')]),
    'payments': ('Pagamento (payments)', 'venda', [
        ('uuid', 'id', 'PK', ''), ('uuid', 'order_id', 'FK', ''),
        ('smallint', 'method', '', 'dinheiro, crédito, débito,<br/>transferência, Pix'), ('numeric', 'amount', '', '')]),
    'promotions': ('Promoção (promotions)', 'venda', [
        ('uuid', 'id', 'PK', ''), ('uuid', 'product_id', 'FK', ''), ('uuid', 'variant_id', 'FK', 'opcional'),
        ('uuid', 'forecast_recommendation_id', 'FK', 'opcional'), ('uuid', 'created_by', 'FK', ''),
        ('numeric', 'discount_percent', '', ''), ('date', 'start_date', '', ''), ('date', 'end_date', '', ''),
        ('varchar', 'reason', '', 'opcional'), ('smallint', 'source', '', 'manual ou da IA'),
        ('bool', 'below_cost_confirmed', '', ''), ('bool', 'is_active', '', ''),
        ('timestamptz', 'canceled_at', '', 'opcional')]),
    'clients': ('Cliente (clients)', 'cadastro', [('uuid', 'id', 'PK', 'detalhado no DER 2')]),
    'users': ('Usuário (users)', 'acesso', [('uuid', 'id', 'PK', 'detalhado no DER 1')]),
    'stores': ('Loja (stores)', 'estoque', [('uuid', 'id', 'PK', 'detalhado no DER 5')]),
    'stock_locations': ('Local de estoque<br/>(stock_locations)', 'estoque', [('uuid', 'id', 'PK', 'detalhado no DER 5')]),
    'products': ('Produto (products)', 'produto', [('uuid', 'id', 'PK', 'detalhado no DER 3')]),
    'product_variants': ('Variação do produto<br/>(product_variants)', 'produto', [('uuid', 'id', 'PK', 'detalhado no DER 3')]),
    'forecast_recommendations': ('Recomendação<br/>(forecast_recommendations)', 'previsao', [('uuid', 'id', 'PK', 'detalhado no DER 9')]),
}

# (pai, cardinalidade no pai, filho, verbo): 1 = exatamente um, 01 = zero ou um; no filho é sempre zero ou muitos
LIGACOES = [
    ('stores', '1', 'orders', 'registra'),
    ('stock_locations', '1', 'orders', 'baixa de'),
    ('clients', '01', 'orders', 'compra'),
    ('users', '1', 'orders', 'vende'),
    ('orders', '1', 'order_items', 'contém'),
    ('orders', '1', 'payments', 'é paga com'),
    ('promotions', '01', 'order_items', 'aplica desconto'),
    ('product_variants', '1', 'order_items', 'é vendida'),
    ('users', '1', 'promotions', 'cria'),
    ('products', '1', 'promotions', 'tem promoções'),
    ('product_variants', '01', 'promotions', 'tem promoção'),
    ('forecast_recommendations', '01', 'promotions', 'gera'),
]

# linhas de cima para baixo (mantém a figura mais alta que larga)
RANKS = [
    ['clients', 'stores', 'stock_locations'],
    ['users', 'orders'],
    ['products', 'forecast_recommendations', 'payments'],
    ['promotions', 'product_variants'],
    ['order_items'],
]

def tabela(nome):
    titulo, modulo, linhas = TABELAS[nome]
    fundo, borda = CORES[modulo]
    cel = '<td align="left" border="1" color="%s" cellpadding="5">%s</td>'
    rows = ['<tr><td colspan="4" bgcolor="%s" border="1" color="%s" cellpadding="7"><b>%s</b></td></tr>' % (fundo, borda, titulo)]
    for i, (tipo, col, chave, coment) in enumerate(linhas):
        bg = ' bgcolor="%s"' % fundo if i % 2 else ''
        rows.append('<tr>' + ''.join((cel % (borda, v or ' ')).replace('<td ', '<td%s ' % bg, 1) for v in (tipo, col, chave, coment)) + '</tr>')
    return '<<table border="2" color="%s" cellborder="0" cellspacing="0" bgcolor="white">%s</table>>' % (borda, ''.join(rows))


def main():
    out = ['digraph der7 {',
           '  graph [rankdir=TB, splines=spline, nodesep=0.35, ranksep=0.75, fontname="Arial", fontsize=26,',
           '         label="Vendas e promoções", labelloc=t, pad=0.3, bgcolor=white];',
           '  node [shape=plaintext, fontname="Arial", fontsize=21];',
           '  edge [fontname="Arial", fontsize=28, color="#555555", penwidth=1.6, dir=both, arrowsize=1.1];']
    for nome in TABELAS:
        out.append('  %s [label=%s];' % (nome, tabela(nome)))
    for r in RANKS:
        out.append('  { rank=same; %s }' % '; '.join(r))
    for pai, card, filho, verbo in LIGACOES:
        tail = 'teetee' if card == '1' else 'teeodot'
        out.append('  %s -> %s [arrowtail=%s, arrowhead=crowodot, label="  %s  "];' % (pai, filho, tail, verbo))
    out.append('}')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
