"""content.json と 5つのトンマナ定義から静的サイトを生成する。

使い方: python3 build.py
"""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).parent
C = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:var(--font-body);line-height:1.8;-webkit-font-smoothing:antialiased}
a{color:inherit}
img{max-width:100%}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
.nav{display:flex;justify-content:space-between;align-items:center;padding:24px 0}
.nav .logo{font-family:var(--font-head);font-weight:700;text-decoration:none}
.nav ul{display:flex;gap:24px;list-style:none;font-size:14px}
.nav ul a{text-decoration:none}
.hero{padding:96px 0 112px}
.hero .role{font-size:14px;letter-spacing:.15em}
.hero h1{font-family:var(--font-head);line-height:1.2;margin:16px 0 24px}
.hero .catch{font-size:clamp(16px,2vw,20px);max-width:640px}
.hero .vol{display:none}
.sec{padding:80px 0}
.sec-title{font-family:var(--font-head);margin-bottom:40px}
.about p{max-width:720px;font-size:17px}
.skills{display:flex;flex-wrap:wrap;gap:12px;list-style:none}
.works{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:28px}
.card{overflow:hidden}
.thumb{aspect-ratio:16/10;display:grid;place-items:center;font-family:var(--font-head);font-size:40px}
.card-body{padding:20px}
.card .tag{font-size:12px;letter-spacing:.1em}
.card h3{font-family:var(--font-head);font-size:20px;margin:6px 0 8px;line-height:1.4}
.card p{font-size:14px}
.contact .mail{font-family:var(--font-head);font-size:clamp(22px,4vw,40px);text-decoration:none;word-break:break-all}
.links{display:flex;gap:20px;margin-top:24px;list-style:none}
footer{padding:40px 0;font-size:13px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px}
@media (max-width:640px){
  .wrap{padding:0 16px}
  .nav ul{gap:14px;font-size:13px}
  .hero{padding:56px 0 72px}
  .sec{padding:56px 0}
  .works{grid-template-columns:1fr}
}
"""

THEMES = [
    {
        "id": "01-minimal",
        "name": "Minimal Mono",
        "jp": "ミニマル・モノトーン",
        "concept": "余白とタイポグラフィだけで語る。情報を整理できる人、という信頼感を出す。",
        "keywords": ["知的", "誠実", "余白", "シンプル"],
        "voice": "言い切り・短文。装飾語を使わない。",
        "colors": [("Ink", "#111111"), ("Paper", "#FFFFFF"), ("Line", "#E5E5E5"), ("Accent", "#FF3B00")],
        "fonts": ("Inter", "Noto Sans JP"),
        "gf": "family=Inter:wght@400;700;800&family=Noto+Sans+JP:wght@400;700",
        "hero": "言葉を、整える。",
        "labels": ("About", "Skills", "Works", "Contact"),
        "css": """
:root{--bg:#fff;--text:#111;--line:#e5e5e5;--accent:#ff3b00;--font-head:'Inter','Noto Sans JP',sans-serif;--font-body:'Noto Sans JP',sans-serif}
.nav{border-bottom:1px solid var(--line)}
.hero h1{font-size:clamp(48px,9vw,120px);font-weight:800;letter-spacing:-.03em}
.hero .role{color:var(--accent)}
.sec{border-top:1px solid var(--line)}
.sec-title{font-size:13px;letter-spacing:.2em;text-transform:uppercase;color:#888;font-weight:400}
.skills li{border:1px solid var(--text);padding:6px 16px;font-size:14px}
.card{border:1px solid var(--line);transition:border-color .2s}
.card:hover{border-color:var(--text)}
.thumb{background:#f4f4f4;color:#ccc;font-weight:800}
.card .tag{color:var(--accent)}
.contact .mail:hover{color:var(--accent)}
footer{border-top:1px solid var(--line);color:#888}
""",
    },
    {
        "id": "02-natural",
        "name": "Warm Natural",
        "jp": "ナチュラル・やさしさ",
        "concept": "生成りとくすみカラーで、相談しやすい温度感。人柄で選ばれたいとき向け。",
        "keywords": ["親しみ", "安心", "丁寧", "あたたかい"],
        "voice": "です・ます調。語りかけるように、やわらかく。",
        "colors": [("Cream", "#F5EFE6"), ("Cocoa", "#5C4A3A"), ("Terracotta", "#C97B4A"), ("Sage", "#8A9A7B")],
        "fonts": ("Zen Maru Gothic", "Zen Maru Gothic"),
        "gf": "family=Zen+Maru+Gothic:wght@400;500;700",
        "hero": "あなたの「伝えたい」に、そっと寄り添います。",
        "labels": ("わたしについて", "できること", "おしごと", "おたより"),
        "css": """
:root{--bg:#f5efe6;--text:#5c4a3a;--accent:#c97b4a;--sage:#8a9a7b;--font-head:'Zen Maru Gothic',sans-serif;--font-body:'Zen Maru Gothic',sans-serif}
.hero{text-align:center}
.hero h1{font-size:clamp(28px,5vw,52px);font-weight:700}
.hero .catch{margin:0 auto}
.hero .role{color:var(--sage)}
.sec-title{font-size:26px;text-align:center;font-weight:700}
.sec-title::after{content:"";display:block;width:40px;height:4px;border-radius:4px;background:var(--accent);margin:12px auto 0}
.about p{margin:0 auto;text-align:center}
.skills{justify-content:center}
.skills li{background:#fff;border-radius:999px;padding:8px 20px;font-size:14px;box-shadow:0 2px 0 #e6dccd}
.card{background:#fff;border-radius:24px;box-shadow:0 6px 24px rgba(92,74,58,.08)}
.card:nth-child(3n+1) .thumb{background:#ead7c3}
.card:nth-child(3n+2) .thumb{background:#dfe4d6}
.card:nth-child(3n) .thumb{background:#f1dfd2}
.thumb{color:rgba(92,74,58,.35)}
.card .tag{color:var(--sage);font-weight:700}
.contact{text-align:center}
.contact .mail{color:var(--accent)}
.links{justify-content:center}
footer{color:#9a8878;justify-content:center}
""",
    },
    {
        "id": "03-pop",
        "name": "Bold Pop",
        "jp": "ポップ・元気",
        "concept": "太い線とビビッドカラーで、一度見たら忘れない。SNS・エンタメ系に強い印象を。",
        "keywords": ["元気", "インパクト", "遊び心", "ワクワク"],
        "voice": "テンポよく！ 体言止めと感嘆符で勢いを出す。",
        "colors": [("Cream", "#FFF4D6"), ("Black", "#1A1A1A"), ("Pink", "#FF5CA8"), ("Blue", "#2D6BFF"), ("Yellow", "#FFD23F")],
        "fonts": ("Dela Gothic One", "M PLUS Rounded 1c"),
        "gf": "family=Dela+Gothic+One&family=M+PLUS+Rounded+1c:wght@500;800",
        "hero": "おもしろいを、言葉にする！",
        "labels": ("ABOUT ME!", "SKILLS!", "WORKS!", "CONTACT!"),
        "css": """
:root{--bg:#fff4d6;--text:#1a1a1a;--pink:#ff5ca8;--blue:#2d6bff;--yellow:#ffd23f;--font-head:'Dela Gothic One',sans-serif;--font-body:'M PLUS Rounded 1c',sans-serif}
body{font-weight:500}
.nav ul a{font-weight:800}
.hero h1{font-size:clamp(44px,8vw,104px);font-weight:400;color:var(--text);text-shadow:5px 5px 0 var(--pink)}
.hero .role{display:inline-block;background:var(--blue);color:#fff;padding:4px 14px;border:3px solid var(--text);border-radius:999px;font-weight:800}
.sec-title{font-size:clamp(32px,5vw,48px);font-weight:400;display:inline-block;background:var(--yellow);padding:4px 16px;border:3px solid var(--text);box-shadow:6px 6px 0 var(--text);transform:rotate(-2deg)}
.skills li{background:#fff;border:3px solid var(--text);border-radius:999px;padding:6px 18px;font-weight:800;box-shadow:3px 3px 0 var(--text)}
.skills li:nth-child(odd){background:var(--pink);color:#fff}
.card{background:#fff;border:3px solid var(--text);border-radius:20px;box-shadow:8px 8px 0 var(--text);transition:transform .15s,box-shadow .15s}
.card:hover{transform:translate(-3px,-3px);box-shadow:11px 11px 0 var(--text)}
.thumb{border-bottom:3px solid var(--text);color:#fff;-webkit-text-stroke:2px var(--text)}
.card:nth-child(3n+1) .thumb{background:var(--pink)}
.card:nth-child(3n+2) .thumb{background:var(--blue)}
.card:nth-child(3n) .thumb{background:var(--yellow)}
.card .tag{font-weight:800;color:var(--blue)}
.contact .mail{background:var(--text);color:var(--yellow);padding:8px 20px;border-radius:16px;display:inline-block}
.links a{font-weight:800}
footer{border-top:3px solid var(--text);font-weight:800}
""",
    },
    {
        "id": "04-tech",
        "name": "Dark Tech",
        "jp": "ダーク・テック",
        "concept": "ターミナル風のダーク基調。AI・自動化に強い専門性をひと目で伝える。",
        "keywords": ["先進的", "専門性", "ロジカル", "クール"],
        "voice": "簡潔・ロジカル。数字と事実で語る。",
        "colors": [("Void", "#0B0F14"), ("Text", "#E6EDF3"), ("Neon", "#39FF88"), ("Signal", "#7AA2FF"), ("Panel", "#151B23")],
        "fonts": ("JetBrains Mono", "Noto Sans JP"),
        "gf": "family=JetBrains+Mono:wght@400;700&family=Noto+Sans+JP:wght@400;700",
        "hero": "AI × 言葉で、仕組みをつくる。",
        "labels": ("// about", "// skills", "// works", "// contact"),
        "css": """
:root{--bg:#0b0f14;--text:#e6edf3;--neon:#39ff88;--signal:#7aa2ff;--panel:#151b23;--line:#253040;--font-head:'JetBrains Mono','Noto Sans JP',monospace;--font-body:'Noto Sans JP',sans-serif}
body{background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:48px 48px;background-attachment:fixed}
body::before{content:"";position:fixed;inset:0;background:radial-gradient(ellipse at top,transparent 0,var(--bg) 70%);pointer-events:none;z-index:-1}
.nav .logo{color:var(--neon)}
.nav .logo::before{content:"> "}
.hero .role{color:var(--neon);font-family:var(--font-head)}
.hero .role::before{content:"$ whoami → "}
.hero h1{font-size:clamp(36px,7vw,84px);font-weight:700}
.hero h1::after{content:"_";color:var(--neon);animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.sec-title{font-size:20px;color:var(--signal);font-weight:400}
.skills li{font-family:var(--font-head);font-size:13px;color:var(--neon);border:1px solid rgba(57,255,136,.4);background:rgba(57,255,136,.06);padding:6px 14px;border-radius:4px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;transition:border-color .2s,box-shadow .2s}
.card:hover{border-color:var(--neon);box-shadow:0 0 24px rgba(57,255,136,.15)}
.thumb{background:linear-gradient(135deg,#0f1a24,#13233a);color:var(--signal);border-bottom:1px solid var(--line)}
.card .tag{font-family:var(--font-head);color:var(--neon)}
.card p{color:#9fb0c0}
.contact .mail{color:var(--neon)}
.links a{font-family:var(--font-head);color:var(--signal)}
footer{border-top:1px solid var(--line);color:#6b7a8a;font-family:var(--font-head)}
""",
    },
    {
        "id": "05-editorial",
        "name": "Elegant Editorial",
        "jp": "エディトリアル・上品",
        "concept": "雑誌の誌面のような明朝体とネイビー×ゴールド。上質さと編集力を印象づける。",
        "keywords": ["上品", "編集力", "大人", "物語性"],
        "voice": "である調、または落ち着いた敬体。余韻を残す一文。",
        "colors": [("Ivory", "#F7F5F0"), ("Navy", "#1D2A44"), ("Gold", "#B08D57"), ("Stone", "#8C8578")],
        "fonts": ("Shippori Mincho", "Shippori Mincho"),
        "gf": "family=Shippori+Mincho:wght@400;600;800&family=Cormorant+Garamond:ital,wght@0,500;1,500",
        "hero": "一行に、物語を。",
        "labels": ("Profile", "Expertise", "Selected Works", "Contact"),
        "css": """
:root{--bg:#f7f5f0;--text:#1d2a44;--gold:#b08d57;--stone:#8c8578;--font-head:'Shippori Mincho',serif;--font-body:'Shippori Mincho',serif;--latin:'Cormorant Garamond',serif}
.nav{border-bottom:1px solid var(--text)}
.nav ul a{font-family:var(--latin);font-size:16px;font-style:italic}
.hero{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:end}
.hero h1{font-size:clamp(44px,8vw,96px);font-weight:600;writing-mode:horizontal-tb}
.hero .role{font-family:var(--latin);font-style:italic;font-size:18px;color:var(--gold);letter-spacing:.05em}
.hero .vol{display:block;font-family:var(--latin);font-size:14px;color:var(--stone);writing-mode:vertical-rl;letter-spacing:.3em}
.sec{border-top:1px solid rgba(29,42,68,.2)}
.sec-title{font-family:var(--latin);font-style:italic;font-weight:500;font-size:clamp(32px,5vw,52px);color:var(--text);display:flex;align-items:baseline;gap:16px}
.sec-title::before{content:attr(data-no);font-size:14px;font-style:normal;color:var(--gold);letter-spacing:.2em}
.about p{font-size:18px;line-height:2.2}
.about p::first-letter{font-size:3em;float:left;line-height:1;margin:6px 10px 0 0;color:var(--gold)}
.skills li{font-size:15px;padding:4px 0;border-bottom:1px solid var(--gold);margin-right:16px}
.works{gap:48px 32px}
.thumb{background:var(--text);color:var(--gold);font-family:var(--latin);font-style:italic;font-size:56px}
.card-body{padding:20px 0}
.card .tag{font-family:var(--latin);font-style:italic;color:var(--gold);font-size:15px}
.card p{color:var(--stone)}
.contact .mail{font-family:var(--latin);font-style:italic;border-bottom:1px solid var(--gold)}
footer{border-top:1px solid var(--text);color:var(--stone)}
@media (max-width:640px){.hero{grid-template-columns:1fr}.hero .vol{display:none}}
""",
    },
]


def portfolio_html(t):
    a, s, w, c = t["labels"]
    skills = "".join(f"<li>{e(x)}</li>" for x in C["skills"])
    works = "".join(
        f'<article class="card"><div class="thumb">{i:02d}</div><div class="card-body">'
        f'<span class="tag">{e(x["tag"])}</span><h3>{e(x["title"])}</h3><p>{e(x["desc"])}</p></div></article>'
        for i, x in enumerate(C["works"], 1)
    )
    links = "".join(f'<li><a href="{e(x["url"])}">{e(x["label"])}</a></li>' for x in C["links"])
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(C["name"])} | Portfolio</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{t["gf"]}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head>
<body><div class="wrap">
<header class="nav"><a class="logo" href="#">{e(C["name_en"])}</a>
<ul><li><a href="#about">{e(a)}</a></li><li><a href="#works">{e(w)}</a></li><li><a href="#contact">{e(c)}</a></li></ul></header>
<section class="hero"><div><p class="role">{e(C["role"])}</p><h1>{e(t["hero"])}</h1><p class="catch">{e(C["name"])}</p></div><span class="vol">PORTFOLIO — VOL.01</span></section>
<section class="sec about" id="about"><h2 class="sec-title" data-no="01">{e(a)}</h2><p>{e(C["about"])}</p></section>
<section class="sec"><h2 class="sec-title" data-no="02">{e(s)}</h2><ul class="skills">{skills}</ul></section>
<section class="sec" id="works"><h2 class="sec-title" data-no="03">{e(w)}</h2><div class="works">{works}</div></section>
<section class="sec contact" id="contact"><h2 class="sec-title" data-no="04">{e(c)}</h2><a class="mail" href="mailto:{e(C["email"])}">{e(C["email"])}</a><ul class="links">{links}</ul></section>
<footer><span>© {e(C["name_en"])}</span><a href="../">← トンマナ一覧へ</a></footer>
</div></body></html>
"""


def index_html():
    cards = ""
    for t in THEMES:
        sw = "".join(
            f'<li><span class="chip" style="background:{h}"></span><b>{e(n)}</b><code>{h}</code></li>' for n, h in t["colors"]
        )
        kw = "".join(f"<span>#{e(k)}</span>" for k in t["keywords"])
        cards += f"""<article class="tm">
<div class="tm-head" style="background:{t["colors"][0][1]};color:{t["colors"][1][1]}">
<span class="no">{t["id"][:2]}</span><h2>{e(t["name"])}</h2><p>{e(t["jp"])}</p></div>
<div class="tm-body"><p class="concept">{e(t["concept"])}</p>
<dl><dt>キーワード</dt><dd class="kw">{kw}</dd>
<dt>カラー</dt><dd><ul class="sw">{sw}</ul></dd>
<dt>フォント</dt><dd>見出し：{e(t["fonts"][0])}<br>本文：{e(t["fonts"][1])}</dd>
<dt>文章トーン</dt><dd>{e(t["voice"])}<br><q>{e(t["hero"])}</q></dd></dl>
<a class="btn" href="{t["id"]}/">このパターンを見る →</a></div></article>"""
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Portfolio Tone &amp; Manner</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Noto Sans JP',sans-serif;background:#f2f2f0;color:#1a1a1a;line-height:1.7}}
header{{max-width:1180px;margin:0 auto;padding:64px 24px 32px}}
header h1{{font-size:clamp(28px,4vw,44px)}}
header p{{color:#666;margin-top:8px}}
main{{max-width:1180px;margin:0 auto;padding:0 24px 80px;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:24px}}
.tm{{background:#fff;border-radius:16px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.tm-head{{padding:28px 24px}}
.tm-head .no{{font-size:13px;opacity:.7}}
.tm-head h2{{font-size:26px;line-height:1.3}}
.tm-head p{{font-size:14px;opacity:.8}}
.tm-body{{padding:24px;display:flex;flex-direction:column;gap:16px;flex:1}}
.concept{{font-size:14px}}
dl{{display:grid;grid-template-columns:84px 1fr;gap:10px 12px;font-size:13px}}
dt{{color:#888;font-weight:700}}
.kw span{{display:inline-block;background:#f2f2f0;border-radius:4px;padding:0 8px;margin:0 4px 4px 0}}
.sw{{list-style:none;display:grid;gap:4px}}
.sw li{{display:flex;align-items:center;gap:8px}}
.chip{{width:18px;height:18px;border-radius:4px;border:1px solid rgba(0,0,0,.12)}}
.sw code{{color:#888;font-size:12px;margin-left:auto}}
q{{display:block;margin-top:4px;font-weight:700}}
.btn{{margin-top:auto;display:block;text-align:center;background:#1a1a1a;color:#fff;text-decoration:none;padding:12px;border-radius:8px;font-weight:700}}
@media (max-width:640px){{header,main{{padding-left:16px;padding-right:16px}}main{{grid-template-columns:1fr}}}}
</style></head><body>
<header><h1>Portfolio — Tone &amp; Manner</h1><p>5つのトンマナで作ったポートフォリオ。気に入ったパターンを選んでください。</p></header>
<main>{cards}</main></body></html>
"""


def main():
    (ROOT / "index.html").write_text(index_html(), encoding="utf-8")
    for t in THEMES:
        d = ROOT / t["id"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(portfolio_html(t), encoding="utf-8")
        (d / "style.css").write_text(BASE_CSS + t["css"], encoding="utf-8")
    print("built", len(THEMES), "patterns")


if __name__ == "__main__":
    main()
