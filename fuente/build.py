import json, re, sys, pathlib
from data import *
NEW = ["Crystal Tree", "Forest Whisper", "Burgundy Cranberry", "Ralph Lauren Style", "Frostbite"]

here = pathlib.Path(__file__).parent
names = here.joinpath("images.txt").read_text().split()
def img(prefix):
    if prefix.startswith("img/"):
        return prefix
    m = [n for n in names if n.startswith(prefix)]
    if len(m) != 1:
        sys.exit(f"image prefix {prefix}: {m}")
    return m[0]

def items(lst):
    out = []
    for n, s, i, _ in lst:
        if isinstance(i, dict):
            out.append({"n": n, "s": [[a, b] for a, b in s], "g": [[img(h), l, t, w] for h, l, t, w in i["g"]], "ar": i["ar"]})
        else:
            out.append({"n": n, "s": [[a, b] for a, b in s], "i": img(i)})
    return out

TREES = {n: {"n": n, "s": s[0][0], "i": img(i)} for n, s, i, _ in ARBOLES}
for _k, _v in COLLECTION_TREE.items():
    assert _v in TREES, _v

data = {
    "collections": [{"name": n, "img": img(i), "tree": t, "sale": s, "rent": r, "note": note, "saleInc": INCLUDES[n][0], "rentInc": INCLUDES[n][1], "tint": TINT[n], "pieces": [[x.rstrip("*"), x.endswith("*")] for x in PIECES.get(n, [])], "items": ITEMS.get(n, []), "extra": EXTRA_PRICE.get(n), "new": n in NEW, "treeItem": TREES.get(COLLECTION_TREE.get(n))}
                    for n, i, t, s, r, note in sorted(COLLECTIONS, key=lambda c: (c[0] not in NEW, NEW.index(c[0]) if c[0] in NEW else 0))],
    "categories": [
        {"id": "arboles", "name": "Árboles", "items": items(ARBOLES)},
        {"id": "esferas", "name": "Esferas y ornamentos", "items": items(ESFERAS)},
        {"id": "follaje", "name": "Follaje y moños", "items": items(FOLLAJE)},
        {"id": "listones", "name": "Listones", "items": items(LISTONES)},
        {"id": "decoraciones", "name": "Decoraciones", "items": items(DECORACIONES)},
    ],
    "install": INSTALACION,
}

BASE = "https://robertagarciabook.my.canva.site/lucypereadecor-catalogo/_assets/media/"
WA = "https://wa.me/525569695206"
WAICON = ('<svg class="ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2l-.5-.3Z"/></svg>')

html = here.joinpath("template.html").read_text()
MENU = here.joinpath("menu.html").read_text()
MAPS = "https://www.google.com/maps/search/?api=1&amp;query=Tlacote+116%2C+Villas+del+Mes%C3%B3n%2C+Juriquilla%2C+Quer%C3%A9taro"
MENU = (MENU.replace("__HOME__#colecciones", "/colecciones/").replace("__HOME__#catalogo", "/catalogo/")
            .replace("__HOME__#cat-", "/catalogo/#cat-").replace("__HOME__", "/"))
html = html.replace("__MENU__", MENU)
NPZ = sum(len(c["items"]) for c in data["categories"])
NWTAG = '<i class="nw">2026</i>'
def _slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower())
def _src(f): return "/" + f if f.startswith("img/") else BASE + f
_ROOT = here.parent
def _cut(f):
    k = "crystal-tree" if "crystal-tree" in f else f[:8]
    return None
def _thumb(c):
    cu = _cut(c["img"])
    return f'<span class="dc-plate"><img class="cut" src="{cu}" alt="" loading="lazy"></span>' if cu else f'<span class="dc-plate ph"><img src="{_src(c["img"])}" alt="" loading="lazy"></span>'
COLTHUMBS = "".join(f'<a class="dc-t" href="/colecciones/#{_slug(c["name"])}">{_thumb(c)}{"<i class=\"nw\">2026</i>" if c["new"] else ""}<span>{c["name"]}</span></a>' for c in data["collections"])
def _bx(c):
    price = f'Venta ${c["sale"]:,}' + (f' · Renta ${c["rent"]:,}' if c["rent"] else "")
    nw = '<span class="nw">Nuevo 2026</span>' if c["new"] else ""
    return f'<a class="bx" href="/colecciones/#{_slug(c["name"])}"><img src="{_src(c["img"])}" alt="Colección {c["name"]}" loading="lazy"><span class="bx-t">{nw}<b>{c["name"]}</b><small>{price}</small></span></a>'
_new = [c for c in data["collections"] if c["new"]][:5]
_rest = [c for c in data["collections"] if c not in _new]
BENTO = "".join(_bx(c) for c in _new)
MORE = "".join(_bx(c) for c in _rest)
CATIMG = {"arboles": "04041766", "esferas": "bb7711bd", "follaje": "96412652", "listones": "39b7fe1d", "decoraciones": "d6b08cb1"}
CATTILES = "".join(f'<a class="dk-t" href="/catalogo/#cat-{c["id"]}"><span class="dk-img"><img src="{BASE + img(CATIMG[c["id"]])}" alt="" loading="lazy"></span><span class="dk-txt"><b>{c["name"]}</b><small>{len(c["items"])} piezas</small></span></a>' for c in data["categories"])
MINSALE = "$" + f'{min(c["sale"] for c in data["collections"]):,}'
MINRENT = "$" + f'{min(c["rent"] for c in data["collections"] if c["rent"]):,}'
html = (html.replace("__NCOL__", str(len(data["collections"]))).replace("__NPZ__", str(NPZ))
            .replace("__COLTHUMBS__", COLTHUMBS).replace("__BENTO__", BENTO).replace("__MORE__", MORE).replace("__CATTILES__", CATTILES)
            .replace("__MINSALE__", MINSALE).replace("__MINRENT__", MINRENT))
html = (html.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
            .replace("__WAICON__", WAICON).replace("__WABASE__", WA).replace("__WA__", WA)
            .replace("__IMGBASE__", BASE).replace("__LOGO__", BASE + img("0a86810f"))
            .replace("__HERO1__", BASE + img("3a75dc37")).replace("__HERO2__", BASE + img("ab12581c"))
            .replace("__HERO3__", BASE + img("08c15db3")))
assert "__" not in re.sub(r"__[a-z]", "", html) or True
full = html
def part(name):
    a = full.index(f"<!--{name}-->"); z = full.index(f"<!--/{name}-->") + len(f"<!--/{name}-->")
    return a, z
def strip(h, name):
    a = h.index(f"  <!--{name}-->"); z = h.index(f"<!--/{name}-->") + len(f"<!--/{name}-->") + 1
    return h[:a] + h[z:]
def inner(name):
    a, z = part(name); return full[a:z]
def links_out(h):
    h = (h.replace('href="#colecciones"', 'href="/colecciones/"').replace('href="#catalogo"', 'href="/catalogo/"')
          .replace('href="#inicio"', 'href="/"'))
    return h
# Página principal: sin colecciones ni catálogo, con las "puertas"
home = links_out(strip(strip(full, "COL"), "CAT"))
here.parent.joinpath("index.html").write_text(home)
# Subpáginas
head = links_out(full[:full.index('<main id="inicio">')])
tail = full[full.index("</main>"):]
def subpage(folder, title, desc, crumb, sect, nxt_href, nxt_label, nxt_kick):
    body = (f'<main id="inicio">\n  <div class="wrap sub-crumb"><a href="/">Inicio</a><span aria-hidden="true">/</span><span>{crumb}</span></div>\n'
            + inner(sect) + f'\n  <div class="wrap sub-next"><a href="{nxt_href}"><span class="label">{nxt_kick}</span><b>{nxt_label} <i aria-hidden="true">→</i></b></a></div>\n'
            + inner("CONTACT") + "\n")
    pg = (head.replace("<title>Lucy Perea Decor · Navidad 2026</title>", f"<title>{title} · Lucy Perea Decor</title>")
              .replace('content="Árboles de Navidad vestidos, esferas, follaje, listones y decoración en existencia. Venta, renta e instalación en Querétaro."', f'content="{desc}"')
          + body + tail)
    ids = set(re.findall(r'id="([^"]+)"', pg))
    pg = re.sub(r'href="#([\w-]+)"', lambda m: m.group(0) if m.group(1) in ids else f'href="/#{m.group(1)}"', pg)
    here.parent.joinpath(folder).mkdir(exist_ok=True)
    here.parent.joinpath(folder, "index.html").write_text(pg)
subpage("colecciones", "Colecciones Navidad 2026", "Colecciones de árboles de Navidad vestidos de Lucy Perea Decor: venta y renta con montaje en Querétaro, CDMX y Estado de México.",
        "Colecciones", "COL", "/catalogo/", "Ver catálogo", "¿Prefieres armar tu propio estilo?")
subpage("catalogo", "Catálogo de piezas", "Catálogo de piezas sueltas de Navidad: árboles, esferas, follaje, listones y decoraciones en existencia. Lucy Perea Decor, Querétaro.",
        "Catálogo", "CAT", "/colecciones/", "Ver colecciones", "¿Buscas un árbol ya vestido?")
html = full

# ---- Subpágina del showroom ----
cut = html.index("\n", html.index(".ico{width:16px")) + 1
basehead = (html[:cut]
    .replace("<title>Lucy Perea Decor · Navidad 2026</title>", "<title>Showroom · Lucy Perea Decor</title>")
    .replace('content="Árboles de Navidad vestidos, esferas, follaje, listones y decoración en existencia. Venta, renta e instalación en Querétaro."',
             'content="Visita el showroom de Lucy Perea Decor en Juriquilla, Querétaro. Árboles de Navidad vestidos y decoración en existencia. Solo con cita."'))
sr = here.joinpath("showroom.html").read_text()
sr = (sr.replace("__BASEHEAD__", basehead).replace("__MENU__", MENU.replace("__HOME__", "/"))
        .replace("__WAICON__", WAICON).replace("__WA__", WA).replace("__MAPS__", MAPS)
        .replace("__LOGO__", BASE + img("0a86810f")))
assert "__" not in sr.replace("__pycache__", ""), [m for m in re.findall(r"__[A-Z]+__", sr)]
here.parent.joinpath("showroom").mkdir(exist_ok=True)
here.parent.joinpath("showroom", "index.html").write_text(sr)
print("ok", len(html), {c["id"]: len(c["items"]) for c in data["categories"]}, len(data["collections"]))
