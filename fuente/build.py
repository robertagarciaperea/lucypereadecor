import json, re, sys, pathlib
from data import *
NEW = ["Forest Whisper", "Burgundy Cranberry", "Ralph Lauren Style", "Frostbite"]

here = pathlib.Path(__file__).parent
names = here.joinpath("images.txt").read_text().split()
def img(prefix):
    m = [n for n in names if n.startswith(prefix)]
    if len(m) != 1:
        sys.exit(f"image prefix {prefix}: {m}")
    return m[0]

def items(lst):
    out = []
    for n, s, i, _ in lst:
        out.append({"n": n, "s": [[a, b] for a, b in s], "i": img(i)})
    return out

data = {
    "collections": [{"name": n, "img": img(i), "tree": t, "sale": s, "rent": r, "note": note, "saleInc": INCLUDES[n][0], "rentInc": INCLUDES[n][1], "tint": TINT[n], "pieces": [[x.rstrip("*"), x.endswith("*")] for x in PIECES[n]], "new": n in NEW}
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
html = (html.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
            .replace("__WAICON__", WAICON).replace("__WABASE__", WA).replace("__WA__", WA)
            .replace("__IMGBASE__", BASE).replace("__LOGO__", BASE + img("0a86810f"))
            .replace("__HERO1__", BASE + img("3a75dc37")).replace("__HERO2__", BASE + img("ab12581c"))
            .replace("__HERO3__", BASE + img("08c15db3")))
assert "__" not in re.sub(r"__[a-z]", "", html) or True
here.parent.joinpath("index.html").write_text(html)
print("ok", len(html), {c["id"]: len(c["items"]) for c in data["categories"]}, len(data["collections"]))
