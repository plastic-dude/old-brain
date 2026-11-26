"""Build the Old Brain SFX library from CC0 packs on OpenGameArt.

Every pack's page is re-read and kept ONLY if CC0 is its sole license (public domain:
safe for a monetized channel AND for committing to this public repo). Writes
sfx/catalog.json (file -> source page, author, license, tags) and sfx/raw/<pack>/...
Run: python tools/sfx_fetch.py [--max-per-keyword N]
"""
import json, re, subprocess, sys, zipfile, io, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "sfx"
UA = {"User-Agent": "Mozilla/5.0 (oldbrain sfx fetch)"}
AUDIO = (".wav", ".ogg", ".mp3", ".flac", ".aif", ".aiff")
# bible beats -> search words
KEYWORDS = {
    "whoosh": ["whoosh", "swoosh", "swish"], "impact": ["punch", "impact", "hit", "thud"],
    "cartoon": ["cartoon", "boing", "spring", "silly", "slide whistle", "squeak"],
    "pop": ["pop", "bubble", "balloon"], "crowd": ["crowd", "applause", "cheer", "laugh"],
    "rumble": ["rumble", "earthquake", "explosion", "meteor"], "stone": ["rock", "stone", "cave"],
    "fire": ["fire", "torch"], "body": ["footsteps", "jump", "fall"], "ui": ["ding", "bell", "notification", "click"],
    "tension": ["drum", "suspense", "heartbeat"], "fail": ["fail", "wrong", "buzzer"],
}
SEED = ["interface-sounds", "rpg-sound-pack", "50-rpg-sound-effects", "impact-sounds", "512-sound-effects-8-bit-style",
        "cartoonish-sound-for-throwing-things", "cartoony-jump-and-bounce", "air-whoosh", "boing", "boings",
        "silly-sound-effects", "spring-sounds", "crowd-shoutingspeaking-ambience", "free-crowd-cheering-sounds",
        "37-hitspunches", "41-random-sound-effects", "background-rumble-noise", "cave-in", "3-pop-sounds",
        "58-random-sound-effects", "a-slide-pop-sound", "balloon-sounds", "bubble-pop", "18-random-video-game-sound-effects"]

def get(url, binary=False, limit=80_000_000):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        if int(r.headers.get("Content-Length") or 0) > limit: raise ValueError("too big")
        data = r.read(limit + 1)
    return data if binary else data.decode("utf-8", "ignore")

def search(word, n):
    q = urllib.parse.quote(word)
    html = get(f"https://opengameart.org/art-search-advanced?keys={q}&field_art_type_tid%5B%5D=13&field_art_license_tid%5B%5D=4&sort_by=count&sort_order=DESC")
    return [s for s in dict.fromkeys(re.findall(r'href="/content/([a-z0-9-]+)"', html)) if s != "faq"][:n]

def pack(slug, tag, cat):
    if slug in cat["packs"]: cat["packs"][slug]["tags"] = sorted(set(cat["packs"][slug]["tags"]) | {tag}); return
    page = f"https://opengameart.org/content/{slug}"; html = get(page)
    lic = set(re.findall(r"(CC0|CC-BY-SA \d\.\d|CC-BY \d\.\d|GPL \d\.\d|LGPL \d\.\d|OGA-BY \d\.\d)", html))
    if lic != {"CC0"}: print("skip (license)", slug, lic); return
    title = (re.search(r"<title>(.*?)\s*\|", html) or [None, slug])[1]
    author = (re.search(r'Author:.*?href="/users/([^"]+)"', html, re.S) or [None, "unknown"])[1]
    urls = [u for u in dict.fromkeys(re.findall(r'https://opengameart.org/sites/default/files/[^"\'<> ]+', html))
            if "/styles/" not in u and "audio_preview" not in u and u.lower().endswith(AUDIO + (".zip",))]
    files = []
    for u in urls:
        try: data = get(u, binary=True)
        except Exception as e: print("fail", u, e); continue
        dest = ROOT / "raw" / slug; dest.mkdir(parents=True, exist_ok=True)
        name = urllib.parse.unquote(u.rsplit("/", 1)[1])
        if name.lower().endswith(".zip"):
            try:
                z = zipfile.ZipFile(io.BytesIO(data))
                for m in z.namelist():
                    if m.lower().endswith(AUDIO) and not m.startswith("__MACOSX"):
                        p = dest / re.sub(r"[^\w.\-]+", "_", m.replace("/", "__")); p.write_bytes(z.read(m)); files.append(str(p.relative_to(ROOT)))
            except zipfile.BadZipFile: print("bad zip", u)
        else:
            p = dest / re.sub(r"[^\w.\-]+", "_", name); p.write_bytes(data); files.append(str(p.relative_to(ROOT)))
    if files:
        cat["packs"][slug] = {"title": title, "author": author, "page": page, "license": "CC0", "tags": [tag], "files": files}
        print(f"ok {slug}: {len(files)} files")

def main():
    n = int(sys.argv[sys.argv.index("--max-per-keyword") + 1]) if "--max-per-keyword" in sys.argv else 6
    ROOT.mkdir(exist_ok=True); cf = ROOT / "catalog.json"
    cat = json.loads(cf.read_text()) if cf.exists() else {"packs": {}}
    for s in SEED:
        try: pack(s, "seed", cat)
        except Exception as e: print("err", s, e)
    for tag, words in KEYWORDS.items():
        for w in words:
            try: slugs = search(w, n)
            except Exception as e: print("search err", w, e); continue
            for s in slugs:
                try: pack(s, tag, cat)
                except Exception as e: print("err", s, e)
            cf.write_text(json.dumps(cat, indent=1))
    total = sum(len(p["files"]) for p in cat["packs"].values())
    print("packs", len(cat["packs"]), "files", total)

if __name__ == "__main__": main()
