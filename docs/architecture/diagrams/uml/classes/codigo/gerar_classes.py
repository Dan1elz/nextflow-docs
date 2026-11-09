#!/usr/bin/env python3
"""
Gera os diagramas de classes (PlantUML) a partir das entidades C# do domínio (nextflow.Domain/Models e Enums).

- Atributos: propriedades públicas de negócio. FK (Guid ...Id) com navegação vira associação, não atributo.
- Associações: navegações (`virtual X` = 1 ou 0..1; `virtual ICollection<X>` = *). Composição onde a parte pertence ao todo.
- Operações: construtores e métodos públicos reais (parâmetros só com o nome); propriedade calculada vira {readOnly}.
- Enums: cada um aparece uma vez, no primeiro módulo que o usa, sem os valores fora do escopo do TCC.
- Cor por módulo, igual ao DER; classe de outro módulo aparece só com o nome e "ver <módulo>".

Uso: python3 gerar_classes.py [--code <caminho do repositório da API>]   (padrão: ../../../../../../../nextflow)
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = Path(sys.argv[sys.argv.index("--code") + 1]) if "--code" in sys.argv else HERE.parents[6] / "nextflow"
MODELS = CODE / "nextflow.Domain/Models"
ENUMS = CODE / "nextflow.Domain/Enums"

# (código, título, cor, classes)
MODULES = [
    ("1-acesso", "Acesso e notificações", "acesso", ["User", "UserStore", "Notification"]),
    ("2-cadastros", "Cadastros de pessoas e localidade", "cadastro",
     ["Client", "Supplier", "Address", "Contact", "City", "State", "Country"]),
    ("3-produto", "Produto, variações e preço", "produto",
     ["Product", "ProductVariant", "ProductAttribute", "ProductAttributeValue", "ProductVariantValue", "PriceHistory"]),
    ("4-classificacao", "Classificação e fornecimento do produto", "produto",
     ["Category", "CategoryProduct", "Collection", "CalendarEvent", "ProductEvent", "ProductSupplier"]),
    ("5-estoque", "Lojas, locais, saldo e livro-razão", "estoque",
     ["Store", "StockLocation", "StockBalance", "Lot", "StockMovement", "StockLocationMinimum", "StockPolicy"]),
    ("6-transferencia", "Transferência de estoque", "estoque", ["StockTransfer", "StockTransferItem"]),
    ("7-vendas", "Vendas e promoções", "venda", ["Order", "OrderItem", "Payment", "Promotion"]),
    ("8-compras", "Pedidos de compra", "compra", ["PurchaseOrder", "PurchaseItem"]),
    ("9-previsao-analise", "Previsão: análise e recomendação", "previsao",
     ["ForecastRun", "ForecastRecommendation", "ForecastAiBatch", "ForecastProjection", "ForecastSettings"]),
    ("10-previsao-aplicacao", "Previsão: aplicação da recomendação", "previsao",
     ["ForecastRecommendationItem", "ForecastRecommendationStore", "ForecastRecommendationPurchaseOrder"]),
    ("11-dados-derivados", "Dados derivados para a previsão", "previsao",
     ["ProductSalesMonthly", "ProductSeasonality", "StockDailySnapshot"]),
]

COLORS = {
    "acesso": ("#FCE4EC", "#F8BBD0", "#C2185B"),
    "cadastro": ("#FFF8E1", "#FFE082", "#F9A825"),
    "produto": ("#EDE7F6", "#D1C4E9", "#5E35B1"),
    "estoque": ("#E8F5E9", "#C8E6C9", "#2E7D32"),
    "venda": ("#E3F2FD", "#BBDEFB", "#1565C0"),
    "compra": ("#FFF3E0", "#FFCC80", "#EF6C00"),
    "previsao": ("#E0F7FA", "#B2EBF2", "#00838F"),
}

PT = {
    "User": "Usuário", "UserStore": "Loja do usuário", "Notification": "Notificação",
    "Client": "Cliente", "Supplier": "Fornecedor", "Address": "Endereço", "Contact": "Contato",
    "City": "Cidade", "State": "Estado", "Country": "País",
    "Product": "Produto", "ProductVariant": "Variação do produto", "ProductAttribute": "Atributo da grade",
    "ProductAttributeValue": "Valor do atributo", "ProductVariantValue": "Valor da variação",
    "PriceHistory": "Histórico de preço", "Category": "Categoria", "CategoryProduct": "Produto na categoria",
    "Collection": "Coleção", "CalendarEvent": "Evento do calendário", "ProductEvent": "Produto no evento",
    "ProductSupplier": "Fornecedor do produto", "Store": "Loja", "StockLocation": "Local de estoque",
    "StockBalance": "Saldo", "Lot": "Lote", "StockMovement": "Movimentação (livro-razão)",
    "StockLocationMinimum": "Mínimo por local", "StockPolicy": "Política de estoque ABC",
    "StockTransfer": "Transferência", "StockTransferItem": "Item da transferência",
    "Order": "Venda", "OrderItem": "Item da venda", "Payment": "Pagamento", "Promotion": "Promoção",
    "PurchaseOrder": "Pedido de compra", "PurchaseItem": "Item do pedido de compra",
    "ForecastRun": "Análise de previsão", "ForecastRecommendation": "Recomendação",
    "ForecastAiBatch": "Lote enviado à IA", "ForecastProjection": "Projeção mensal",
    "ForecastSettings": "Agendamento da previsão", "ForecastRecommendationItem": "Item da recomendação",
    "ForecastRecommendationStore": "Parte da loja na compra",
    "ForecastRecommendationPurchaseOrder": "Pedido gerado pela recomendação",
    "ProductSalesMonthly": "Venda mensal do produto", "ProductSeasonality": "Sazonalidade do produto",
    "StockDailySnapshot": "Fotografia diária do estoque",
}

# Navegações que são composição (a parte não existe sem o todo): (classe, navegação)
COMPOSITIONS = {
    ("Order", "Items"), ("Order", "Payments"), ("PurchaseOrder", "Items"), ("StockTransfer", "Items"),
    ("Product", "Variants"), ("Product", "Attributes"), ("ProductAttribute", "Values"),
    ("ProductVariant", "AttributeValues"), ("ProductVariant", "PriceHistory"), ("ProductVariant", "LocationMinimums"),
    ("Store", "Locations"), ("Country", "States"), ("State", "Cities"),
    ("ForecastRun", "Recommendations"), ("ForecastRun", "Batches"), ("ForecastRun", "Projections"),
    ("ForecastRecommendation", "Items"), ("ForecastRecommendation", "Stores"),
    ("ForecastRecommendation", "PurchaseOrders"),
}

# Valores de enum fora do escopo do TCC (existem no código, não são usados).
HIDDEN_ENUM_VALUES = {
    "OrderStatusEnum": {"Budget", "Refunded", "Expired"}, "OrderChannelEnum": {"Order"},
    "SourceTypeEnum": {"InventoryCount"}, "MovementReasonEnum": {"CountAdjustment"}, "RoleEnum": {"User"},
}

# Nome curto do módulo para o "ver ..." das classes de referência.
SHORT = {"1-acesso": "Acesso", "2-cadastros": "Cadastros", "3-produto": "Produto", "4-classificacao": "Classificação",
         "5-estoque": "Estoque", "6-transferencia": "Transferência", "7-vendas": "Vendas", "8-compras": "Compras",
         "9-previsao-analise": "Previsão (análise)", "10-previsao-aplicacao": "Previsão (aplicação)",
         "11-dados-derivados": "Dados derivados"}

# Dono polimórfico (OwnerType + OwnerId, sem navegação): (classe, donos)
POLYMORPHIC = [("Address", ["Client", "Supplier"]), ("Contact", ["Client", "Supplier"])]

# Colunas da figura de enumerações (módulos empilhados em cada coluna)
ENUM_COLUMNS = [["1-acesso", "2-cadastros", "3-produto", "4-classificacao", "5-estoque", "7-vendas", "8-compras",
                 "9-previsao-analise"]]

SKIP_MEMBERS = {"Preposition", "Singular", "Plural", "UpdatedAt", "CreatedAt", "Version"}

PROP = re.compile(r"^\s*public\s+(?P<virtual>virtual\s+)?(?P<type>[\w<>?,\[\]. ]+?)\s+(?P<name>[A-Z]\w*)\s*(\{\s*get|=>)")
METHOD = re.compile(r"^\s*public\s+(?P<static>static\s+)?(?:(?P<ret>[\w<>?,\[\]. ]+?)\s+)?(?P<name>[A-Z]\w*)\s*\(")
CLASS = re.compile(r"^public\s+(?:abstract\s+|sealed\s+)?class\s+(\w+)")


def parse_models():
    classes = {}
    for f in sorted(MODELS.glob("*.cs")):
        lines = f.read_text().splitlines()
        current = None
        i = 0
        while i < len(lines):
            line = lines[i]
            m = CLASS.match(line)
            if m:
                current = dict(name=m.group(1), props=[], navs=[], ops=[])
                classes[current["name"]] = current
                i += 1
                continue
            if current is None or "override" in line or " const " in line:
                i += 1
                continue
            p = PROP.match(line)
            if p and p.group("name") not in SKIP_MEMBERS:
                typ = p.group("type").strip()
                computed = "=>" in line.split(p.group("name"), 1)[1][:6] or "{ get; }" in line
                if p.group("virtual"):
                    coll = re.match(r"ICollection<(\w+)>", typ)
                    target = coll.group(1) if coll else typ.rstrip("?")
                    current["navs"].append(dict(name=p.group("name"), target=target, many=bool(coll),
                                                optional=typ.endswith("?")))
                else:
                    current["props"].append(dict(name=p.group("name"), type=typ, computed=computed))
                i += 1
                continue
            mm = METHOD.match(line)
            if mm and not line.strip().startswith("public class"):
                # junta a assinatura até fechar os parênteses
                sig, j = line, i
                while sig.count("(") > sig.count(")") and j + 1 < len(lines):
                    j += 1
                    sig += " " + lines[j].strip()
                params = sig[sig.index("(") + 1: sig.index(")")]
                parts = [re.split(r"\s+", x.strip().split("=")[0].strip()) for x in params.split(",") if x.strip()]
                names = [p[-1] for p in parts]
                types = [" ".join(p[:-1]) for p in parts]
                current["ops"].append(dict(name=mm.group("name"), ret=(mm.group("ret") or "").strip(),
                                           static=bool(mm.group("static")), params=names, types=types,
                                           ctor=mm.group("name") == current["name"]))
                i = j + 1
                continue
            i += 1
    return classes


def parse_enums():
    enums = {}
    for f in sorted(ENUMS.glob("*.cs")):
        text = f.read_text()
        m = re.search(r"public enum (\w+)[^{]*\{([^}]*)\}", text)
        if m:
            values = re.findall(r"^\s*([A-Z]\w*)\s*=", m.group(2), re.M)
            enums[m.group(1)] = [v for v in values if v not in HIDDEN_ENUM_VALUES.get(m.group(1), set())]
    return enums


def fk_props(cls):
    """Guid ...Id que tem navegação correspondente (vira associação, não atributo)."""
    nav_names = {n["name"] for n in cls["navs"]}
    return {p["name"] for p in cls["props"]
            if p["type"].startswith("Guid") and p["name"].endswith("Id") and p["name"][:-2] in nav_names}


def module_of(name):
    for code, title, color, members in MODULES:
        if name in members:
            return code, title, color
    return None, None, None


def header():
    out = ["!include ../../estilo.iuml", "skinparam dpi 170", "skinparam classAttributeIconSize 0",
           "skinparam class {", "  BorderThickness 1.4", "  FontSize 14", "  AttributeFontSize 13", "}",
           "hide empty members"]
    for color, (bg, head, border) in COLORS.items():
        out += [f"skinparam class<<{color}>> {{", f"  BackgroundColor {bg}", f"  HeaderBackgroundColor {head}",
                f"  BorderColor {border}", "}", f"hide <<{color}>> stereotype"]
    return out


def op_text(op, typed=False):
    params = ", ".join(f"{n} : {t}" if typed else n for n, t in zip(op["params"], op["types"]))
    if op["ctor"]:
        return f"  + {op['name']}({params})"
    ret = f" : {op['ret']}" if op["ret"] else ""
    static = "{static} " if op["static"] else ""
    return f"  + {static}{op['name']}({params}){ret}"


def class_block(cls, color):
    fks = fk_props(cls)
    pt = PT.get(cls["name"], "")
    out = [f'class "{cls["name"]}\\n<size:11><i>{pt}</i></size>" as {cls["name"]} <<{color}>> {{']
    for p in cls["props"]:
        if p["name"] in fks:
            continue
        ro = " {readOnly}" if p["computed"] else ""
        out.append(f"  + {p['name']} : {p['type']}{ro}")
    out.append("  --")
    keys = [(op["name"], tuple(op["params"])) for op in cls["ops"]]
    out += [op_text(op, typed=keys.count((op["name"], tuple(op["params"]))) > 1) for op in cls["ops"]]
    out.append("}")
    return "\n".join(out)


def module_puml(code, title, color, members, classes, enums, enum_home):
    out = [f"@startuml classes-{code}"] + header() + [f"title <size:20>Classes — {title}</size>", ""]
    refs, used_enums = set(), []
    for name in members:
        out.append(class_block(classes[name], color))
        for p in classes[name]["props"]:
            base = p["type"].rstrip("?")
            if base in enums and enum_home.get(base) == code and base not in used_enums:
                used_enums.append(base)
    # Enums ficam na figura própria (enumerações); aqui o tipo aparece só no atributo.
    # associações
    drawn = set()
    lines = []
    for name in members:
        cls = classes[name]
        for nav in cls["navs"]:
            target = nav["target"]
            if target not in classes:
                continue
            key = frozenset((name, target, nav["name"]))
            if target not in members:
                refs.add(target)
            if nav["many"]:
                # coleção: o lado "um" é este; procura a navegação inversa para a multiplicidade do outro lado
                back = next((n for n in classes[target]["navs"] if n["target"] == name and not n["many"]), None)
                one = "0..1" if back and back["optional"] else "1"
                rel = "*--" if (name, nav["name"]) in COMPOSITIONS else "--"
                arrow = "" if back else ">"
                lines.append(f'{name} "{one}" {rel}{arrow} "*" {target} : {nav["name"]}')
                if back:
                    drawn.add((target, back["name"]))
            else:
                if (name, nav["name"]) in drawn:
                    continue
                inverse = next((n for n in classes[target]["navs"] if n["target"] == name and n["many"]), None)
                if inverse and target in members:
                    continue  # desenhada pelo lado da coleção
                mult = "0..1" if nav["optional"] else "1"
                lines.append(f'{name} "*" --> "{mult}" {target} : {nav["name"]}')
            drawn.add((name, nav["name"]))
    for r in sorted(refs):
        rcode, _rtitle, rcolor = module_of(r)
        out.append(f'class "{r}\\n<size:11><i>ver {SHORT.get(rcode, rcode)}</i></size>" as {r} <<{rcolor or color}>>')
    out.append("")
    out += lines
    for part, owners in POLYMORPHIC:
        if part in members:
            out += [f'{o} "1" .. "*" {part} : OwnerType + OwnerId' for o in owners if o in members]
    out.append('note as Base\n  Todas herdam de <b>BaseModel</b> (Id : Guid, CreatedAt : DateTime).\n'
               '  Atributos com set privado: só o construtor e os métodos mudam o estado.\nend note')
    out.append("@enduml\n")
    # remove dependências repetidas
    seen, result = set(), []
    for line in "\n".join(out).split("\n"):
        if "..>" in line and line in seen:
            continue
        seen.add(line)
        result.append(line)
    return "\n".join(result)


def enums_puml(enums, enum_home):
    """Figura única com os enums do domínio, agrupados pelo módulo onde aparecem primeiro."""
    out = ["@startuml classes-12-enumeracoes"] + header() + ["title <size:20>Enumerações do domínio</size>", ""]
    color_of = {code: color for code, _t, color, _m in MODULES}
    for column in ENUM_COLUMNS:
        for code in column:
            names = [e for e, home in enum_home.items() if home == code]
            if not names:
                continue
            out.append(f'package "{SHORT[code]}" <<Rectangle>> {{')
            for e in names:
                out.append(f"  enum {e} <<{color_of[code]}>> {{\n" + "\n".join(f"    {v}" for v in enums[e]) + "\n  }")
            out.append("}")
            # empilha os enums do módulo em colunas de até 4 (ligações invisíveis)
            for i in range(len(names) - 1):
                if (i + 1) % 4:
                    out.append(f"{names[i]} -[hidden]down- {names[i + 1]}")
    out.append("note as Fora\n  Valores fora do escopo do TCC omitidos: orçamento, reembolso e expiração\n"
               "  na venda, inventário no livro-razão e perfil User.\nend note")
    out.append("@enduml\n")
    return "\n".join(out)


def main():
    classes = parse_models()
    enums = parse_enums()
    all_members = [m for _c, _t, _co, members in MODULES for m in members]
    missing = sorted(set(classes) - set(all_members) - {"BaseModel"})
    if missing:
        raise SystemExit(f"Classes sem módulo: {missing}")
    unknown = sorted(set(all_members) - set(classes))
    if unknown:
        raise SystemExit(f"Classes do mapa que não existem no código: {unknown}")
    enum_home = {}
    for code, _t, _c, members in MODULES:
        for name in members:
            for p in classes[name]["props"]:
                base = p["type"].rstrip("?")
                if base in enums:
                    enum_home.setdefault(base, code)
    for code, title, color, members in MODULES:
        (HERE / f"classes-{code}.puml").write_text(module_puml(code, title, color, members, classes, enums, enum_home))
    (HERE / "classes-12-enumeracoes.puml").write_text(enums_puml(enums, enum_home))
    print(f"{len(MODULES)} figuras + enumerações; {len(classes) - 1} classes, {len(enum_home)} enums.")


if __name__ == "__main__":
    main()
