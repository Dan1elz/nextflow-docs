#!/usr/bin/env python3
"""
Gera os DERs em Mermaid (erDiagram) a partir do esquema real do banco, no estilo didático do TCC:
nome em português, cor por módulo, verbo em cada ligação, comentário nos enums e sem colunas de auditoria.

Entrada (./esquema, extraída do Postgres de dev com as migrations aplicadas; comandos no README):
  colunas.txt  tabela|coluna|tipo|nulo|tamanho|posição|precisão|escala
  chaves.txt   tabela|coluna|tabela_referenciada|PRIMARY KEY/FOREIGN KEY/UNIQUE
Saída: der-<n>-<módulo>.mmd (um por escopo) e der-apendice-geral.mmd (mapa dos módulos).

Uso: python3 gerar_der.py   (depois renderizar com o mermaid-cli; ver README)
"""
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent

# ---------------------------------------------------------------- módulos: (código, título, cor, tabelas, referências)
MODULES = [
    ("1-acesso", "Acesso e notificações", "acesso", ["users", "user_stores", "notifications"], ["stores"]),
    ("2-cadastros", "Cadastros de pessoas e localidade", "cadastro",
     ["clients", "suppliers", "addresses", "contacts", "cities", "states", "countries"], []),
    ("3-produto", "Produto, variações e preço", "produto",
     ["products", "product_variants", "product_attributes", "product_attribute_values",
      "product_variant_values", "price_history"], ["users"]),
    ("4-classificacao", "Classificação e fornecimento do produto", "produto",
     ["categories", "category_products", "collections", "calendar_events", "product_events",
      "product_suppliers"], ["products", "suppliers"]),
    ("5-estoque", "Lojas, locais, saldo e livro-razão", "estoque",
     ["stores", "stock_locations", "stock_balances", "lots", "stock_movements",
      "stock_location_minimums", "stock_policies"], ["product_variants", "users"]),
    ("6-transferencia", "Transferência de estoque", "estoque",
     ["stock_transfers", "stock_transfer_items"],
     ["stock_locations", "product_variants", "users", "forecast_recommendations"]),
    ("7-vendas", "Vendas e promoções", "venda",
     ["orders", "order_items", "payments", "promotions"],
     ["clients", "users", "stores", "stock_locations", "products", "product_variants", "forecast_recommendations"]),
    ("8-compras", "Pedidos de compra", "compra",
     ["purchase_orders", "purchase_items"],
     ["suppliers", "stores", "stock_locations", "users", "product_variants"]),
    ("9-previsao-analise", "Previsão de demanda com IA: análise e recomendação", "previsao",
     ["forecast_runs", "forecast_recommendations", "forecast_ai_batches", "forecast_projections", "forecast_settings"],
     ["products", "users"]),
    ("10-previsao-aplicacao", "Previsão de demanda com IA: aplicação da recomendação", "previsao",
     ["forecast_recommendation_items", "forecast_recommendation_stores", "forecast_recommendation_purchase_orders"],
     ["forecast_recommendations", "product_variants", "stores", "purchase_orders", "promotions", "stock_transfers",
      "stock_locations"]),
    ("11-dados-derivados", "Dados derivados para a previsão", "previsao",
     ["product_sales_monthly", "product_seasonality", "stock_daily_snapshots"],
     ["products", "product_variants", "stock_locations"]),
]

# Cores por módulo (iguais em todas as figuras): fundo, borda.
COLORS = {
    "acesso": ("#FCE4EC", "#C2185B"),
    "cadastro": ("#FFF8E1", "#F9A825"),
    "produto": ("#EDE7F6", "#5E35B1"),
    "estoque": ("#E8F5E9", "#2E7D32"),
    "venda": ("#E3F2FD", "#1565C0"),
    "compra": ("#FFF3E0", "#EF6C00"),
    "previsao": ("#E0F7FA", "#00838F"),
}

NAMES = {
    "users": "Usuário", "user_stores": "Loja do usuário", "notifications": "Notificação",
    "clients": "Cliente", "suppliers": "Fornecedor", "addresses": "Endereço", "contacts": "Contato",
    "cities": "Cidade", "states": "Estado", "countries": "País",
    "products": "Produto", "product_variants": "Variação do produto", "product_attributes": "Atributo da grade",
    "product_attribute_values": "Valor do atributo", "product_variant_values": "Valor da variação",
    "price_history": "Histórico de preço",
    "categories": "Categoria", "category_products": "Produto na categoria", "collections": "Coleção",
    "calendar_events": "Evento do calendário", "product_events": "Produto no evento",
    "product_suppliers": "Fornecedor do produto",
    "stores": "Loja", "stock_locations": "Local de estoque", "stock_balances": "Saldo", "lots": "Lote",
    "stock_movements": "Movimentação - livro-razão", "stock_location_minimums": "Mínimo por local",
    "stock_policies": "Política de estoque ABC",
    "stock_transfers": "Transferência", "stock_transfer_items": "Item da transferência",
    "orders": "Venda", "order_items": "Item da venda", "payments": "Pagamento", "promotions": "Promoção",
    "purchase_orders": "Pedido de compra", "purchase_items": "Item do pedido de compra",
    "forecast_runs": "Análise de previsão", "forecast_recommendations": "Recomendação",
    "forecast_recommendation_items": "Item da recomendação", "forecast_recommendation_stores": "Parte da loja na compra",
    "forecast_recommendation_purchase_orders": "Pedido gerado pela recomendação",
    "forecast_ai_batches": "Lote enviado à IA", "forecast_projections": "Projeção mensal",
    "forecast_settings": "Agendamento da previsão",
    "product_sales_monthly": "Venda mensal do produto", "product_seasonality": "Sazonalidade do produto",
    "stock_daily_snapshots": "Fotografia diária do estoque",
}

# Verbo de cada ligação, lido do pai para o filho ("Loja possui Local").
VERBS = {
    ("user_stores", "user_id"): "trabalha em", ("user_stores", "store_id"): "tem equipe",
    ("notifications", "user_id"): "recebe",
    ("cities", "state_id"): "contém", ("states", "country_id"): "contém", ("addresses", "city_id"): "localiza",
    ("product_variants", "product_id"): "tem variações", ("product_attributes", "product_id"): "define a grade",
    ("product_attribute_values", "attribute_id"): "tem valores",
    ("product_variant_values", "variant_id"): "combina", ("product_variant_values", "attribute_value_id"): "compõe",
    ("price_history", "variant_id"): "tem preços", ("price_history", "changed_by"): "altera",
    ("products", "collection_id"): "agrupa",
    ("categories", "parent_id"): "é pai de",
    ("category_products", "category_id"): "classifica", ("category_products", "product_id"): "está em",
    ("product_events", "event_id"): "puxa a venda de", ("product_events", "product_id"): "vende em",
    ("product_suppliers", "product_id"): "é comprado de", ("product_suppliers", "supplier_id"): "fornece",
    ("stock_locations", "store_id"): "possui",
    ("stores", "default_sale_location_id"): "é local padrão de venda",
    ("stores", "default_receive_location_id"): "é local padrão de recebimento",
    ("stock_balances", "location_id"): "guarda", ("stock_balances", "variant_id"): "tem saldo",
    ("stock_balances", "lot_id"): "separa por lote",
    ("lots", "variant_id"): "tem lotes",
    ("stock_movements", "location_id"): "movimenta", ("stock_movements", "variant_id"): "movimenta",
    ("stock_movements", "lot_id"): "de qual lote", ("stock_movements", "user_id"): "lança",
    ("stock_location_minimums", "location_id"): "define mínimo", ("stock_location_minimums", "variant_id"): "tem mínimo",
    ("stock_daily_snapshots", "location_id"): "fotografa", ("stock_daily_snapshots", "variant_id"): "fotografa",
    ("stock_transfers", "from_location_id"): "sai de", ("stock_transfers", "to_location_id"): "entra em",
    ("stock_transfers", "created_by"): "registra", ("stock_transfers", "forecast_recommendation_id"): "gera",
    ("stock_transfer_items", "transfer_id"): "contém", ("stock_transfer_items", "variant_id"): "é transferida",
    ("orders", "client_id"): "compra", ("orders", "user_id"): "vende", ("orders", "store_id"): "registra",
    ("orders", "sale_location_id"): "baixa de",
    ("order_items", "order_id"): "contém", ("order_items", "variant_id"): "é vendida",
    ("order_items", "promotion_id"): "aplica desconto",
    ("payments", "order_id"): "é paga com",
    ("promotions", "product_id"): "tem promoções", ("promotions", "variant_id"): "tem promoção",
    ("promotions", "created_by"): "cria", ("promotions", "forecast_recommendation_id"): "gera",
    ("purchase_orders", "supplier_id"): "recebe pedidos", ("purchase_orders", "store_id"): "compra para",
    ("purchase_orders", "receive_location_id"): "recebe em", ("purchase_orders", "created_by"): "cria",
    ("purchase_orders", "received_by"): "recebe",
    ("purchase_items", "purchase_order_id"): "contém", ("purchase_items", "variant_id"): "é comprada",
    ("forecast_runs", "requested_by"): "pede",
    ("forecast_settings", "updated_by"): "configura",
    ("forecast_ai_batches", "forecast_run_id"): "envia à IA",
    ("forecast_projections", "forecast_run_id"): "projeta", ("forecast_projections", "product_id"): "é projetado",
    ("forecast_recommendations", "forecast_run_id"): "recomenda",
    ("forecast_recommendations", "product_id"): "recebe recomendação",
    ("forecast_recommendations", "applied_by"): "aplica",
    ("forecast_recommendations", "applied_purchase_order_id"): "nasceu de",
    ("forecast_recommendations", "applied_promotion_id"): "nasceu de",
    ("forecast_recommendations", "applied_transfer_id"): "nasceu de",
    ("forecast_recommendations", "transfer_from_location_id"): "origem da transferência",
    ("forecast_recommendations", "transfer_to_location_id"): "destino da transferência",
    ("forecast_recommendation_items", "recommendation_id"): "rateia nas variações",
    ("forecast_recommendation_items", "variant_id"): "recebe parte",
    ("forecast_recommendation_stores", "recommendation_id"): "divide por loja",
    ("forecast_recommendation_stores", "store_id"): "recebe parte",
    ("forecast_recommendation_purchase_orders", "recommendation_id"): "gera pedidos",
    ("forecast_recommendation_purchase_orders", "purchase_order_id"): "veio da recomendação",
    ("product_sales_monthly", "product_id"): "vende por mês", ("product_seasonality", "product_id"): "tem sazonalidade",
}

# Significado das colunas codificadas (enums smallint) e de outras que pedem explicação.
COMMENTS = {
    "users.role": "perfil: só Administrador",
    "addresses.owner_type": "dono: cliente ou fornecedor", "contacts.owner_type": "dono: cliente ou fornecedor",
    "addresses.owner_id": "id do cliente ou fornecedor", "contacts.owner_id": "id do cliente ou fornecedor",
    "contacts.type": "telefone, e-mail ou WhatsApp",
    "calendar_events.scope": "nacional ou da empresa",
    "calendar_events.date_rule": "fixa, Páscoa, n-ésimo dia, Black Friday",
    "calendar_events.lead_days": "dias antes em que a venda sobe",
    "forecast_ai_batches.status": "pendente, enviado, concluído, falhou",
    "forecast_recommendations.action": "comprar, promover, manter, transferir",
    "forecast_recommendations.priority": "baixa, média, alta",
    "forecast_recommendations.confidence": "baixa, média, alta",
    "forecast_recommendations.status": "pendente, aplicada, descartada, expirada",
    "forecast_recommendations.lead_time_source": "de onde veio o prazo de entrega",
    "forecast_recommendations.dismiss_reason_code": "motivo do descarte",
    "forecast_runs.trigger": "manual ou agendada",
    "forecast_runs.status": "em andamento, concluída, sem IA, falhou",
    "forecast_runs.horizon_months": "meses projetados",
    "forecast_settings.weekday": "dia da análise semanal",
    "notifications.type": "recomendações, lote vencendo, estoque baixo",
    "orders.status": "paga ou cancelada",
    "orders.channel": "balcão",
    "payments.method": "dinheiro, crédito, débito, transferência, Pix",
    "products.product_type": "padrão, vestuário, perecível, granel",
    "products.sale_unit": "unidade, kg, litro, metro",
    "products.lifecycle": "em linha ou fora de linha",
    "products.abc_class": "curva ABC",
    "products.decimal_places": "casas decimais da quantidade",
    "promotions.source": "manual ou da IA",
    "purchase_orders.status": "orçamento, pendente, recebido, cancelado",
    "stock_movements.type": "entrada ou saída",
    "stock_movements.reason": "compra, venda, transferência, perda...",
    "stock_movements.source_type": "tipo do documento de origem",
    "stock_movements.source_id": "id do documento de origem",
    "stock_movements.balance_after": "saldo depois do lançamento",
    "stock_policies.abc_class": "A, B ou C",
    "stock_locations.is_sellable": "vende neste local?",
    "product_suppliers.is_preferred": "fornecedor preferido",
    "forecast_ai_batches.product_ids": "produtos enviados no lote",
}

AUDIT = {"created_at", "updated_at", "version"}

# Referência "pivô": tabela de outra figura cujas FKs também são desenhadas aqui (com as colunas dessas FKs).
PIVOTS = {"10-previsao-aplicacao": ["forecast_recommendations"]}

# Ligações sem FK física (dono polimórfico): (tabela, destinos, verbo)
POLYMORPHIC = [
    ("addresses", ["clients", "suppliers"], "tem endereços"),
    ("contacts", ["clients", "suppliers"], "tem contatos"),
]


def figure_of(table):
    for code, _t, _c, tables, _r in MODULES:
        if table in tables:
            return int(code.split("-")[0])
    return 0


def color_of(table):
    for _code, _t, color, tables, _r in MODULES:
        if table in tables:
            return color
    return "estoque"


def load():
    cols = defaultdict(list)
    for line in (HERE / "esquema/colunas.txt").read_text().splitlines():
        p = line.split("|")
        if len(p) < 8:
            continue
        table, col, typ, nullable, _length, pos, _prec, _scale = p[:8]
        cols[table].append(dict(name=col, type=fmt_type(typ), null=nullable == "YES", pos=int(pos)))
    pk, fk = defaultdict(set), []
    for line in (HERE / "esquema/chaves.txt").read_text().splitlines():
        p = line.split("|")
        if len(p) < 4:
            continue
        table, col, ref, kind = p[:4]
        if kind == "PRIMARY KEY":
            pk[table].add(col)
        elif kind == "FOREIGN KEY" and ref:
            fk.append((table, col, ref))
    return cols, pk, sorted(set(fk))


def fmt_type(typ):
    # Tipos sem parênteses (o erDiagram não aceita "varchar(100)"); tamanho e precisão ficam no esquema extraído.
    return {
        "character varying": "varchar", "timestamp with time zone": "timestamptz",
        "time without time zone": "time", "integer": "int", "boolean": "bool", "ARRAY": "uuid_array",
    }.get(typ, typ)


def label(table):
    return f"{NAMES.get(table, table)} ({table})"


def entity(table, cols, pk, fks):
    fk_cols = {c for t, c, _ in fks if t == table}
    lines = [f'    {table}["{label(table)}"] {{']
    ordered = sorted(
        (c for c in cols[table] if c["name"] not in AUDIT),
        key=lambda c: (0 if c["name"] in pk[table] else 1 if c["name"] in fk_cols else 2, c["pos"]),
    )
    for c in ordered:
        key = "PK" if c["name"] in pk[table] else "FK" if c["name"] in fk_cols else ""
        notes = [COMMENTS.get(f"{table}.{c['name']}", "")]
        if c["null"] and c["name"] not in pk[table]:
            notes.append("opcional")
        note = ", ".join(n for n in notes if n)
        lines.append(f'        {c["type"]} {c["name"]}' + (f" {key}" if key else "") + (f' "{note}"' if note else ""))
    lines.append("    }")
    return "\n".join(lines)


def ref_entity(table, fk_cols=()):
    lines = [f'    {table}["{label(table)}"] {{', f'        uuid id PK "detalhado no DER {figure_of(table)}"']
    lines += [f"        uuid {c} FK \"opcional\"" for c in fk_cols]
    lines.append("    }")
    return "\n".join(lines)


def relation(child, col, parent, cols):
    nullable = next((c["null"] for c in cols[child] if c["name"] == col), False)
    left = "|o" if nullable else "||"
    return f'    {parent} {left}--o{{ {child} : "{VERBS[(child, col)]}"'


HEADER = """---
title: "{title}"
config:
  er:
    layoutDirection: TB
  themeVariables:
    fontFamily: Arial
    fontSize: 20px
---
erDiagram"""


def module_mmd(code, title, tables, refs, cols, pk, fks):
    shown = set(tables) | set(refs)
    pivots = PIVOTS.get(code, [])
    drawn = [(c, col, p) for c, col, p in fks
             if p in shown and (c in tables or (c in pivots and p != c))]
    out = [HEADER.format(title=title)]
    out += [entity(t, cols, pk, fks) for t in tables]
    out += [ref_entity(r, [col for c, col, _p in drawn if c == r]) for r in refs]
    out.append("")
    out += [relation(c, col, p, cols) for c, col, p in drawn]
    for child, targets, verb in POLYMORPHIC:
        if child in tables:
            out += [f'    {t} ||..o{{ {child} : "{verb}"' for t in targets if t in shown]
    by_color = defaultdict(list)
    for t in sorted(shown):
        by_color[color_of(t)].append(t)
    out.append("")
    for color, members in by_color.items():
        fill, stroke = COLORS[color]
        out.append(f"    classDef {color} fill:{fill},stroke:{stroke},stroke-width:2px")
        out.append(f"    class {','.join(members)} {color}")
    return "\n".join(out) + "\n"


def appendix_mmd(fks):
    """Mapa dos módulos (flowchart): cada caixa lista as tabelas; a seta diz quantas FKs ligam um módulo ao outro."""
    module_of = {t: code for code, _ti, _c, tables, _r in MODULES for t in tables}
    out = ["---", 'title: "Mapa geral dos módulos do banco (apêndice)"', "config:", "  themeVariables:",
           "    fontFamily: Arial", "    fontSize: 18px", "---", "flowchart TB"]
    for code, title, color, tables, _r in MODULES:
        n = code.split("-")[0]
        body = "<br/>".join(sorted(tables))
        out.append(f'    m{n}["<b>{n}. {title}</b><br/><br/>{body}"]:::{color}')
    links = defaultdict(int)
    for child, _col, parent in fks:
        a, b = module_of[child], module_of[parent]
        if a != b and parent != "users":  # autoria (created_by...) liga tudo a users: vai no texto
            links[(a, b)] += 1
    for (a, b), n in sorted(links.items()):
        out.append(f'    m{a.split("-")[0]} -->|"{n} FK{"s" if n > 1 else ""}"| m{b.split("-")[0]}')
    for color, (fill, stroke) in COLORS.items():
        out.append(f"    classDef {color} fill:{fill},stroke:{stroke},stroke-width:2px")
    return "\n".join(out) + "\n"


def main():
    cols, pk, fks = load()
    covered = {t for _c, _ti, _co, tables, _r in MODULES for t in tables}
    missing = set(cols) - covered
    if missing:
        raise SystemExit(f"Tabelas sem módulo: {sorted(missing)}")
    no_verb = [(c, col) for c, col, _p in fks if (c, col) not in VERBS]
    if no_verb:
        raise SystemExit(f"FKs sem verbo: {no_verb}")
    no_name = sorted(covered - set(NAMES))
    if no_name:
        raise SystemExit(f"Tabelas sem nome em português: {no_name}")
    for code, title, _color, tables, refs in MODULES:
        (HERE / f"der-{code}.mmd").write_text(module_mmd(code, title, tables, refs, cols, pk, fks))
    (HERE / "der-apendice-geral.mmd").write_text(appendix_mmd(fks))
    print(f"{len(MODULES)} figuras + apêndice; {len(covered)} tabelas, {len(fks)} chaves estrangeiras.")


if __name__ == "__main__":
    main()
