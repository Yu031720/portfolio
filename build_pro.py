"""企業サイト水準の5パターン（pro/）を生成する。

使い方: python3 build_pro.py
"""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "pro"
C = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--text);font-family:var(--font-body);font-size:15px;line-height:1.85;letter-spacing:.02em;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
ul{list-style:none}
.wrap{max-width:var(--max,1200px);margin:0 auto;padding:0 40px}
.util{font-size:12px;background:var(--util-bg);color:var(--util-text)}
.util .wrap{display:flex;justify-content:flex-end;gap:24px;height:36px;align-items:center}
.gh{position:sticky;top:0;z-index:10;background:var(--head-bg);border-bottom:1px solid var(--line)}
.gh .wrap{display:flex;align-items:center;height:72px;gap:40px}
.logo{font-family:var(--font-head);font-weight:700;font-size:20px;display:flex;align-items:center;gap:10px;white-space:nowrap}
.logo i{width:28px;height:28px;display:inline-block;background:var(--accent)}
.gnav{display:flex;gap:32px;font-size:14px;margin-left:auto}
.gnav a{position:relative;padding:4px 0}
.gnav a::after{content:"";position:absolute;left:0;right:0;bottom:-2px;height:2px;background:var(--accent);transform:scaleX(0);transition:transform .25s}
.gnav a:hover::after{transform:scaleX(1)}
.btn{display:inline-flex;align-items:center;gap:12px;padding:14px 28px;font-size:14px;font-weight:700;transition:all .2s;white-space:nowrap}
.btn::after{content:"→";transition:transform .2s}
.btn:hover::after{transform:translateX(4px)}
.btn-primary{background:var(--accent);color:var(--on-accent)}
.btn-ghost{border:1px solid currentColor}
.hero{position:relative;overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center;min-height:560px;padding-top:72px;padding-bottom:72px}
.eyebrow{font-size:12px;letter-spacing:.2em;font-weight:700;color:var(--accent-text)}
.hero h1{font-family:var(--font-head);font-size:clamp(34px,5vw,64px);line-height:1.25;margin:20px 0 24px;letter-spacing:.01em}
.hero .lead{font-size:16px;max-width:520px;opacity:.85}
.hero .cta{display:flex;gap:16px;margin-top:40px;flex-wrap:wrap}
.visual{position:relative;aspect-ratio:1/1;width:100%}
.visual span{position:absolute;display:block}
.notice{border-bottom:1px solid var(--line)}
.notice .wrap{display:flex;gap:24px;align-items:center;height:56px;font-size:13px;overflow:hidden;white-space:nowrap}
.notice b{color:var(--accent-text);font-size:12px;letter-spacing:.1em}
.notice time{opacity:.6}
.sec{padding:120px 0}
.sec-head{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;margin-bottom:56px;flex-wrap:wrap}
.sec-head .en{font-size:12px;letter-spacing:.2em;font-weight:700;color:var(--accent-text);display:block;margin-bottom:12px}
.sec-head h2{font-family:var(--font-head);font-size:clamp(26px,3.2vw,40px);line-height:1.35}
.more{font-size:14px;font-weight:700;display:inline-flex;gap:8px;align-items:center}
.more::after{content:"→"}
.stats{display:grid;grid-template-columns:repeat(4,1fr)}
.stat{padding:40px 32px}
.stat b{display:block;font-family:var(--font-num,var(--font-head));font-size:clamp(32px,4vw,52px);line-height:1.1;font-weight:700}
.stat span{font-size:13px;opacity:.75}
.services{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.svc{padding:40px 32px;display:flex;flex-direction:column;gap:16px;transition:all .25s}
.svc .no{font-family:var(--font-num,var(--font-head));font-size:13px;font-weight:700;color:var(--accent-text)}
.svc h3{font-family:var(--font-head);font-size:20px;line-height:1.5}
.svc p{font-size:14px;opacity:.8}
.about .wrap{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center}
.about-vis{aspect-ratio:4/3;position:relative;overflow:hidden}
.about p{font-size:16px;line-height:2.1}
.skills{display:flex;flex-wrap:wrap;gap:8px;margin-top:32px}
.skills li{font-size:12px;padding:6px 14px}
.works{display:grid;grid-template-columns:repeat(3,1fr);gap:40px 28px}
.work .thumb{aspect-ratio:16/10;position:relative;overflow:hidden;margin-bottom:20px}
.work .thumb::before{content:"";position:absolute;inset:0;transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.work:hover .thumb::before{transform:scale(1.06)}
.work .tag{font-size:11px;letter-spacing:.15em;font-weight:700;color:var(--accent-text)}
.work h3{font-family:var(--font-head);font-size:18px;margin:6px 0 6px;line-height:1.5}
.work p{font-size:13px;opacity:.75}
.news li a{display:grid;grid-template-columns:120px 110px 1fr 24px;gap:24px;align-items:center;padding:24px 8px;border-bottom:1px solid var(--line);transition:background .2s}
.news li:first-child a{border-top:1px solid var(--line)}
.news li a::after{content:"→";color:var(--accent-text)}
.news time{font-family:var(--font-num,var(--font-head));font-size:14px;opacity:.7}
.news .cat{font-size:11px;text-align:center;padding:3px 0;border:1px solid var(--line)}
.ctaband{padding:96px 0}
.ctaband .wrap{display:flex;justify-content:space-between;align-items:center;gap:40px;flex-wrap:wrap}
.ctaband h2{font-family:var(--font-head);font-size:clamp(24px,3vw,36px);line-height:1.4}
.ctaband p{opacity:.8;margin-top:8px}
.gf{padding:80px 0 32px;font-size:13px;background:var(--foot-bg);color:var(--foot-text)}
.gf .cols{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:40px;padding-bottom:56px}
.gf h4{font-size:13px;margin-bottom:16px}
.gf li{margin-bottom:10px;opacity:.75}
.gf li a:hover{opacity:1;text-decoration:underline}
.gf .copy{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:24px;border-top:1px solid rgba(128,128,128,.25);opacity:.7;font-size:12px}
.reveal{opacity:0;transform:translateY(24px);transition:opacity .8s ease,transform .8s cubic-bezier(.2,.7,.2,1)}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}
@media (max-width:960px){
  .gnav{display:none}
  .gh .btn{margin-left:auto}
  .hero .wrap,.about .wrap{grid-template-columns:1fr;gap:48px}
  .visual{max-width:420px;margin:0 auto}
  .stats{grid-template-columns:repeat(2,1fr)}
  .services,.works{grid-template-columns:1fr 1fr}
  .gf .cols{grid-template-columns:1fr 1fr}
}
@media (max-width:640px){
  .wrap{padding:0 16px}
  body{font-size:14px}
  .util{display:none}
  .gh .wrap{height:60px;gap:16px}
  .gh .btn{padding:10px 16px;font-size:12px}
  .hero .wrap{min-height:0;padding-top:48px;padding-bottom:56px}
  .sec{padding:72px 0}
  .stat{padding:28px 16px}
  .services,.works{grid-template-columns:1fr}
  .news li a{grid-template-columns:1fr auto;gap:6px 16px;padding:18px 4px}
  .news .cat{display:none}
  .news li a span:last-of-type{grid-column:1/-1}
  .news li a::after{display:none}
  .ctaband{padding:64px 0}
  .gf .cols{grid-template-columns:1fr}
}
"""

THEMES = [
    {
        "id": "01-precision",
        "industry": "テック・家電・高級ブランド",
        "head": ("#000000", "#FFFFFF"),
        "name": "Precision Black",
        "jp": "精密・プレミアム",
        "ref": "大手エレクトロニクスメーカーの製品サイト",
        "concept": "黒を基調に、光と余白で「精度の高さ」を見せる。一流メーカーのような静かな自信。",
        "keywords": ["プレミアム", "精密", "高級感", "静けさ"],
        "colors": [("Black", "#000000"), ("Graphite", "#1C1C1E"), ("White", "#FFFFFF"), ("Champagne", "#C9A96E")],
        "fonts": ("Inter", "Noto Sans JP"),
        "gf": "family=Inter:wght@300;400;600;700&family=Noto+Sans+JP:wght@300;400;700",
        "eyebrow": "CREATIVE × TECHNOLOGY",
        "hero": "言葉に、\n精度を。",
        "lead": "テクノロジーと編集の視点で、伝わる体験を設計する。",
        "css": """
:root{--bg:#000;--text:#f5f5f7;--line:rgba(255,255,255,.12);--accent:#fff;--on-accent:#000;--accent-text:#c9a96e;--util-bg:#000;--util-text:#8e8e93;--head-bg:rgba(0,0,0,.8);--foot-bg:#0a0a0a;--foot-text:#a1a1a6;--font-head:'Inter','Noto Sans JP',sans-serif;--font-body:'Noto Sans JP',sans-serif;--font-num:'Inter',sans-serif;--max:1280px}
.gh{backdrop-filter:saturate(180%) blur(20px)}
.logo{font-weight:600;letter-spacing:.25em;font-size:16px;text-transform:uppercase}
.logo i{display:none}
.gnav{font-size:13px;color:#d1d1d6}
.btn{border-radius:0;font-weight:600;letter-spacing:.05em}
.btn-ghost{color:#fff}
.hero h1{font-weight:300;font-size:clamp(44px,7vw,96px);white-space:pre-line;letter-spacing:-.01em}
.hero .lead{color:#a1a1a6}
.visual span:nth-child(1){inset:8%;border-radius:50%;background:radial-gradient(circle at 35% 30%,#3a3a3c 0,#111 45%,#000 70%);box-shadow:inset -20px -30px 60px rgba(0,0,0,.9),0 0 120px rgba(201,169,110,.25)}
.visual span:nth-child(2){inset:8%;border-radius:50%;background:conic-gradient(from 200deg,transparent 0 70%,rgba(201,169,110,.55) 80%,transparent 90%);filter:blur(8px);animation:spin 12s linear infinite}
.visual span:nth-child(3){left:0;right:0;top:50%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.4),transparent)}
@keyframes spin{to{transform:rotate(360deg)}}
.notice{background:#0a0a0a}
.stats{border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.stat+.stat{border-left:1px solid var(--line)}
.stat b{font-weight:300}
.svc{background:#111;border:1px solid #1c1c1e}
.svc:hover{background:#1c1c1e}
.about-vis{background:linear-gradient(160deg,#1c1c1e,#000);border:1px solid var(--line)}
.about-vis::before{content:"";position:absolute;left:10%;right:10%;top:45%;height:24%;background:linear-gradient(90deg,#2a2a2c,#5a5a5e,#2a2a2c);border-radius:6px;box-shadow:0 40px 80px rgba(201,169,110,.2)}
.skills li{border:1px solid var(--line);color:#d1d1d6}
.work .thumb::before{background:radial-gradient(circle at 70% 30%,#c9a96e33,transparent 60%),linear-gradient(140deg,#1c1c1e,#000)}
.work:nth-child(2n) .thumb::before{background:radial-gradient(circle at 30% 70%,#ffffff22,transparent 55%),linear-gradient(200deg,#2c2c2e,#000)}
.news li a:hover{background:#111}
.ctaband{background:linear-gradient(120deg,#2a2218,#000 60%)}
""",
    },
    {
        "id": "02-trust",
        "industry": "金融・保険・士業・不動産",
        "head": ("#0B5A45", "#FFFFFF"),
        "name": "Trust Green",
        "jp": "信頼・誠実",
        "ref": "メガバンクのコーポレートサイト",
        "concept": "深いグリーンと整った情報設計で「この人なら任せられる」という安心感をつくる。",
        "keywords": ["信頼", "誠実", "わかりやすさ", "安定"],
        "colors": [("Deep Green", "#0B5A45"), ("Fresh Green", "#9BC31C"), ("Mint", "#EEF5F1"), ("Ink", "#222222")],
        "fonts": ("Noto Sans JP", "Noto Sans JP"),
        "gf": "family=Noto+Sans+JP:wght@400;500;700&family=Roboto:wght@500;700",
        "eyebrow": "FOR YOUR BUSINESS",
        "hero": "伝わる言葉で、\nビジネスを前へ。",
        "lead": "ライティングと生成AIの活用で、お客さまの発信と業務をしっかり支えます。",
        "css": """
:root{--bg:#fff;--text:#222;--line:#dfe6e2;--accent:#0b5a45;--on-accent:#fff;--accent-text:#0b5a45;--util-bg:#f4f7f5;--util-text:#555;--head-bg:#fff;--foot-bg:#0b3d30;--foot-text:#e6efe9;--font-head:'Noto Sans JP',sans-serif;--font-body:'Noto Sans JP',sans-serif;--font-num:'Roboto',sans-serif}
.logo i{border-radius:50%;background:conic-gradient(#9bc31c 0 25%,#0b5a45 0)}
.gnav{font-weight:500}
.btn{border-radius:999px}
.btn-ghost{color:#0b5a45;border-color:#0b5a45;background:#fff}
.hero{background:linear-gradient(180deg,#eef5f1,#fff)}
.hero h1{white-space:pre-line;color:#0b5a45;font-weight:700}
.visual span:nth-child(1){inset:4% 4% 4% 4%;border-radius:40px;background:linear-gradient(145deg,#0b5a45,#127a5d);box-shadow:0 30px 60px rgba(11,90,69,.25)}
.visual span:nth-child(2){width:46%;aspect-ratio:1;right:-2%;bottom:-2%;border-radius:50%;background:#9bc31c;opacity:.9}
.visual span:nth-child(3){left:14%;top:16%;width:52%;height:34%;border-radius:16px;background:rgba(255,255,255,.95);box-shadow:0 12px 30px rgba(0,0,0,.15)}
.visual span:nth-child(3)::before{content:"";position:absolute;left:12%;right:12%;top:26%;height:10%;border-radius:4px;background:#0b5a45;box-shadow:0 22px 0 #dfe6e2,0 40px 0 #dfe6e2}
.notice{background:#fff}
.notice b{background:#0b5a45;color:#fff;padding:2px 10px;border-radius:999px}
.sec:nth-of-type(even){background:#f4f7f5}
.sec-head .en{color:#9bc31c}
.sec-head h2{padding-left:20px;border-left:4px solid #0b5a45}
.stats{gap:16px}
.stat{background:#fff;border-radius:12px;border:1px solid var(--line);text-align:center}
.stat b{color:#0b5a45}
.svc{background:#fff;border:1px solid var(--line);border-radius:16px;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.svc:hover{border-color:#0b5a45;box-shadow:0 12px 30px rgba(11,90,69,.12);transform:translateY(-4px)}
.svc .no{display:inline-grid;place-items:center;width:44px;height:44px;border-radius:50%;background:#eef5f1}
.about-vis{border-radius:24px;background:linear-gradient(135deg,#eef5f1,#d6eadf)}
.about-vis::before{content:"";position:absolute;width:60%;aspect-ratio:1;border-radius:50%;left:20%;top:10%;background:radial-gradient(circle,#9bc31c 0 30%,transparent 31%),#0b5a45;opacity:.9}
.skills li{background:#eef5f1;color:#0b5a45;border-radius:999px;font-weight:500}
.work .thumb{border-radius:16px}
.work .thumb::before{background:linear-gradient(135deg,#0b5a45,#127a5d)}
.work:nth-child(3n+2) .thumb::before{background:linear-gradient(135deg,#9bc31c,#5f9a1a)}
.work:nth-child(3n) .thumb::before{background:linear-gradient(135deg,#d6eadf,#eef5f1)}
.news .cat{border-radius:4px;background:#eef5f1;border-color:#eef5f1;color:#0b5a45}
.news li a:hover{background:#f4f7f5}
.ctaband{background:#0b5a45;color:#fff}
.ctaband .btn-primary{background:#fff;color:#0b5a45}
""",
    },
    {
        "id": "03-vivid",
        "name": "Vivid Coral",
        "jp": "元気・親しみ",
        "ref": "勢いのあるスタートアップやD2Cブランドのサイト",
        "industry": "スタートアップ・飲食・ライフスタイル",
        "head": ("#FF5A36", "#FFFFFF"),
        "concept": "コーラルとサニーイエローの明るい配色で、前向きなエネルギーと親しみやすさを届ける。",
        "keywords": ["元気", "親しみ", "前向き", "スピード感"],
        "colors": [("Coral", "#FF5A36"), ("Sunny", "#FFC531"), ("Peach", "#FFF3EC"), ("Cocoa", "#1F1A17")],
        "fonts": ("Inter", "Noto Sans JP"),
        "gf": "family=Inter:wght@400;600;700;800&family=Noto+Sans+JP:wght@400;500;700;900",
        "eyebrow": "PORTFOLIO 2026",
        "hero": "書く。考える。\nそして、つくる。",
        "lead": "言葉とAIで、毎日の仕事をもっと楽しく、もっと速く。",
        "css": """
:root{--bg:#fff;--text:#1f1a17;--line:#f1e4dc;--accent:#ff5a36;--on-accent:#fff;--accent-text:#e8461f;--util-bg:#fff3ec;--util-text:#7a6a62;--head-bg:rgba(255,255,255,.85);--foot-bg:#1f1a17;--foot-text:#e9dcd4;--font-head:'Inter','Noto Sans JP',sans-serif;--font-body:'Noto Sans JP',sans-serif;--font-num:'Inter',sans-serif;--max:1120px}
.util{display:none}
.gh{backdrop-filter:saturate(180%) blur(20px)}
.logo{font-weight:800}
.logo i{border-radius:10px;background:linear-gradient(135deg,#ff5a36,#ffc531)}
.gnav{font-weight:500}
.gnav a::after{height:3px;border-radius:3px}
.btn{border-radius:999px;font-weight:700}
.btn-ghost{color:#1f1a17;border:2px solid #1f1a17}
.hero{background:#fff3ec}
.hero .wrap{grid-template-columns:1fr;text-align:center;min-height:0;padding-top:96px;padding-bottom:0;gap:48px}
.hero h1{font-weight:900;font-size:clamp(40px,7vw,84px);white-space:pre-line;letter-spacing:-.01em;line-height:1.15}
.hero .lead{margin:0 auto;font-size:clamp(16px,2vw,20px)}
.hero .cta{justify-content:center}
.visual{aspect-ratio:21/9;max-width:none}
.visual span:nth-child(1){left:8%;right:8%;top:14%;bottom:0;border-radius:32px 32px 0 0;background:#ff5a36}
.visual span:nth-child(2){width:26%;aspect-ratio:1;border-radius:50%;background:#ffc531;right:4%;top:0;box-shadow:0 20px 40px rgba(255,90,54,.25)}
.visual span:nth-child(3){left:18%;top:30%;width:40%;height:44%;border-radius:20px;background:#fff;box-shadow:0 20px 40px rgba(0,0,0,.12)}
.visual span:nth-child(3)::before{content:"";position:absolute;left:10%;top:18%;width:30%;height:14%;border-radius:999px;background:#ffc531;box-shadow:0 44px 0 -4px #f1e4dc,90px 44px 0 -4px #f1e4dc}
.notice{background:#fff;border:0}
.notice .wrap{justify-content:center}
.notice b{background:#ffc531;color:#1f1a17;padding:2px 12px;border-radius:999px}
.sec-head{flex-direction:column;align-items:center;text-align:center}
.sec-head h2{font-weight:900;font-size:clamp(30px,4.5vw,46px)}
.stats{gap:20px}
.stat{background:#fff3ec;border-radius:28px;text-align:center;padding:48px 24px}
.stat b{font-weight:800;color:#ff5a36}
.services{gap:20px}
.svc{background:#fff;border:2px solid #1f1a17;border-radius:28px;padding:44px 32px;box-shadow:6px 6px 0 #1f1a17}
.svc:hover{transform:translate(-3px,-3px);box-shadow:9px 9px 0 #ff5a36}
.svc .no{display:inline-grid;place-items:center;width:48px;height:48px;border-radius:50%;background:#ffc531;color:#1f1a17}
.svc h3{font-size:22px;font-weight:800}
.about{background:#fff3ec}
.about-vis{border-radius:32px;background:#ffc531}
.about-vis::before{content:"";position:absolute;width:64%;aspect-ratio:1;border-radius:50%;left:18%;top:14%;background:#ff5a36}
.about-vis::after{content:"";position:absolute;width:30%;aspect-ratio:1;border-radius:24px;right:8%;bottom:8%;background:#fff;transform:rotate(12deg)}
.skills li{background:#fff;border-radius:999px;font-weight:700}
.works{gap:24px}
.work{background:#fff3ec;border-radius:28px;padding:14px 14px 28px;transition:transform .25s}
.work:hover{transform:translateY(-4px)}
.work .thumb{border-radius:18px}
.work .thumb::before{background:#ff5a36}
.work:nth-child(3n+2) .thumb::before{background:#ffc531}
.work:nth-child(3n) .thumb::before{background:#1f1a17}
.work .tag,.work h3,.work p{padding:0 10px}
.work h3{font-weight:800}
.news .cat{border:0;background:#fff3ec;border-radius:999px;color:#e8461f;font-weight:700}
.news li a:hover{background:#fff3ec}
.ctaband{background:#ff5a36;color:#fff;text-align:center}
.ctaband .wrap{flex-direction:column;justify-content:center}
.ctaband .btn-primary{background:#1f1a17}
""",
    },
    {
        "id": "04-consulting",
        "industry": "コンサル・BtoB・IT企業",
        "head": ("#051C2C", "#FFFFFF"),
        "name": "Consulting Navy",
        "jp": "知性・戦略",
        "ref": "外資系コンサルティングファームのサイト",
        "concept": "ネイビーと明朝の見出しで、論理と洞察を語るプロフェッショナルの佇まいを。",
        "keywords": ["知性", "戦略的", "権威", "洞察"],
        "colors": [("Navy", "#051C2C"), ("Electric", "#2251FF"), ("Cyan", "#00A9F4"), ("Paper", "#FFFFFF")],
        "fonts": ("Noto Serif JP", "Noto Sans JP"),
        "gf": "family=Noto+Serif+JP:wght@500;700&family=Noto+Sans+JP:wght@400;700&family=Source+Serif+4:wght@600",
        "eyebrow": "INSIGHTS / WRITING / AI",
        "hero": "言葉は、\n戦略である。",
        "lead": "情報を構造化し、意思決定を動かすコンテンツを。リサーチから執筆、AIによる仕組み化まで。",
        "css": """
:root{--bg:#fff;--text:#051c2c;--line:#d0d5da;--accent:#2251ff;--on-accent:#fff;--accent-text:#2251ff;--util-bg:#051c2c;--util-text:#a8b3bd;--head-bg:#fff;--foot-bg:#051c2c;--foot-text:#c5ced6;--font-head:'Noto Serif JP',serif;--font-body:'Noto Sans JP',sans-serif;--font-num:'Source Serif 4',serif}
.logo{font-family:'Source Serif 4','Noto Serif JP',serif;font-size:22px}
.logo i{width:4px;height:28px;background:#2251ff}
.gnav{font-weight:700;font-size:13px}
.btn{border-radius:0}
.btn-ghost{color:#fff}
.hero{background:#051c2c;color:#fff}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(115deg,transparent 55%,rgba(34,81,255,.35) 75%,rgba(0,169,244,.25));pointer-events:none}
.hero h1{white-space:pre-line;font-weight:500;font-size:clamp(40px,6vw,80px)}
.hero .lead{color:#c5ced6}
.eyebrow{color:#00a9f4}
.visual span:nth-child(1){left:6%;right:6%;bottom:8%;height:70%;background:repeating-linear-gradient(0deg,rgba(255,255,255,.08) 0 1px,transparent 1px 25%)}
.visual span:nth-child(2){left:12%;bottom:8%;width:12%;height:30%;background:#00a9f4;box-shadow:80px -40px 0 0 #2251ff,160px -100px 0 0 #fff}
.visual span:nth-child(3){left:6%;right:6%;top:18%;height:2px;background:linear-gradient(90deg,#00a9f4,#2251ff);transform:rotate(-14deg);transform-origin:left}
.notice{background:#f0f2f4}
.sec-head{border-bottom:1px solid #051c2c;padding-bottom:24px}
.sec-head h2{font-weight:500}
.stats{border-top:4px solid #051c2c}
.stat b{font-weight:600;color:#2251ff}
.stat+.stat{border-left:1px solid var(--line)}
.services{gap:0;border-top:1px solid var(--line)}
.svc{border-right:1px solid var(--line);padding:40px 32px 48px}
.svc:last-child{border-right:0}
.svc:hover{background:#f0f2f4}
.svc .no{font-family:'Source Serif 4',serif;font-size:40px;color:#051c2c;line-height:1}
.svc h3{font-weight:500}
.about{background:#f0f2f4}
.about-vis{background:#051c2c}
.about-vis::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 75% 30%,#2251ff 0,transparent 45%),radial-gradient(circle at 20% 80%,#00a9f4 0,transparent 40%);opacity:.8}
.about p{font-family:'Noto Serif JP',serif}
.skills li{border:1px solid #051c2c;font-weight:700}
.work .thumb::before{background:linear-gradient(135deg,#051c2c 40%,#2251ff)}
.work:nth-child(3n+2) .thumb::before{background:linear-gradient(135deg,#2251ff,#00a9f4)}
.work:nth-child(3n) .thumb::before{background:linear-gradient(135deg,#d0d5da,#f0f2f4)}
.work h3{font-weight:500}
.news .cat{border-color:#051c2c;font-weight:700}
.news li a:hover{background:#f0f2f4}
.ctaband{background:#2251ff;color:#fff}
.ctaband .btn-primary{background:#fff;color:#051c2c}
""",
    },
    {
        "id": "05-beauty",
        "name": "Blush Beauty",
        "jp": "やわらか・上品",
        "ref": "コスメブランドやビューティーサロンのサイト",
        "industry": "美容・サロン・ウェルネス・ファッション",
        "head": ("#F3DCE0", "#3D2A33"),
        "concept": "ブラッシュピンクとローズ、明朝体の繊細さで、女性向けブランドにふさわしい上品なやわらかさを。",
        "keywords": ["上品", "やわらか", "女性らしさ", "透明感"],
        "colors": [("Blush", "#F3DCE0"), ("Rose", "#C2577A"), ("Champagne", "#D9B99B"), ("Plum", "#3D2A33")],
        "fonts": ("Shippori Mincho", "Noto Sans JP"),
        "gf": "family=Shippori+Mincho:wght@500;700&family=Noto+Sans+JP:wght@400;500&family=Cormorant+Garamond:ital,wght@1,500",
        "eyebrow": "BEAUTY & LIFESTYLE",
        "hero": "美しさを、\n言葉で届ける。",
        "lead": "ブランドの世界観に寄り添い、読む人の心に残る言葉を丁寧に紡ぎます。",
        "css": """
:root{--bg:#fbf4f2;--text:#3d2a33;--line:#ead6d6;--accent:#c2577a;--on-accent:#fff;--accent-text:#c2577a;--util-bg:#f3dce0;--util-text:#7d5f6a;--head-bg:rgba(251,244,242,.9);--foot-bg:#3d2a33;--foot-text:#ead6d6;--font-head:'Shippori Mincho',serif;--font-body:'Noto Sans JP',sans-serif;--font-num:'Cormorant Garamond',serif;--max:1120px}
body{letter-spacing:.06em}
.gh{backdrop-filter:blur(16px)}
.logo{font-weight:500;letter-spacing:.15em}
.logo i{width:18px;height:18px;border-radius:50% 50% 50% 0;background:linear-gradient(135deg,#f3dce0,#c2577a)}
.gnav{font-size:13px;letter-spacing:.12em}
.btn{border-radius:999px;font-weight:500;letter-spacing:.12em}
.btn-ghost{color:#3d2a33;border-color:#c2577a}
.hero{background:linear-gradient(180deg,#f3dce0,#fbf4f2)}
.hero h1{white-space:pre-line;font-weight:500;letter-spacing:.1em;line-height:1.6}
.eyebrow{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;font-size:16px;letter-spacing:.15em}
.visual span:nth-child(1){left:20%;right:20%;top:4%;bottom:4%;border-radius:999px 999px 24px 24px;background:linear-gradient(180deg,#e8b4c0,#c2577a)}
.visual span:nth-child(2){width:34%;aspect-ratio:1;border-radius:50%;left:6%;bottom:6%;background:radial-gradient(circle at 35% 35%,#fff,#d9b99b);box-shadow:0 20px 40px rgba(194,87,122,.25)}
.visual span:nth-child(3){right:28%;top:18%;writing-mode:vertical-rl;font-family:'Shippori Mincho',serif;font-size:clamp(16px,1.8vw,22px);letter-spacing:.5em;color:#fff}
.visual span:nth-child(3)::before{content:"言葉をまとう"}
.notice{background:#fbf4f2}
.notice b{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:15px}
.sec-head{flex-direction:column;align-items:center;text-align:center}
.sec-head .en{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:18px;font-weight:500;letter-spacing:.1em}
.sec-head h2{font-weight:500;letter-spacing:.12em}
.stats{gap:16px}
.stat{text-align:center;background:#fff;border-radius:999px 999px 24px 24px;padding:56px 16px 40px}
.stat b{font-weight:500;color:#c2577a;font-style:italic}
.svc{background:#fff;border-radius:24px;text-align:center;align-items:center}
.svc:hover{box-shadow:0 20px 40px rgba(194,87,122,.15);transform:translateY(-4px)}
.svc .no{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:28px}
.svc h3{font-weight:500}
.about{background:#f3dce0}
.about-vis{border-radius:999px 999px 24px 24px;background:linear-gradient(180deg,#fff,#ead6d6);aspect-ratio:3/4;max-height:520px}
.about-vis::before{content:"";position:absolute;width:44%;aspect-ratio:1;border-radius:50%;left:28%;top:30%;background:radial-gradient(circle at 35% 35%,#fff,#d9b99b)}
.about p{font-family:'Shippori Mincho',serif;line-height:2.4}
.skills li{background:#fff;border-radius:999px;color:#7d5f6a}
.work .thumb{border-radius:200px 200px 16px 16px}
.work .thumb::before{background:linear-gradient(180deg,#f3dce0,#e8b4c0)}
.work:nth-child(3n+2) .thumb::before{background:linear-gradient(180deg,#f5ece4,#d9b99b)}
.work:nth-child(3n) .thumb::before{background:linear-gradient(180deg,#e8b4c0,#c2577a)}
.work{text-align:center}
.work .tag{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:14px}
.work h3{font-weight:500}
.news .cat{border-radius:999px;border-color:#e8b4c0;color:#c2577a}
.news li a:hover{background:#f3dce0}
.ctaband{background:linear-gradient(135deg,#c2577a,#3d2a33);color:#fff}
.ctaband .btn-primary{background:#fff;color:#c2577a}
""",
    },
]


def page(t):
    stats = "".join(f'<div class="stat reveal"><b>{e(s["num"])}</b><span>{e(s["label"])}</span></div>' for s in C["stats"])
    svcs = "".join(
        f'<article class="svc reveal"><span class="no">{i:02d}</span><h3>{e(s["title"])}</h3><p>{e(s["desc"])}</p></article>'
        for i, s in enumerate(C["services"], 1)
    )
    skills = "".join(f"<li>{e(x)}</li>" for x in C["skills"])
    works = "".join(
        f'<a class="work reveal" href="#"><div class="thumb"></div><span class="tag">{e(w["tag"].upper())}</span>'
        f'<h3>{e(w["title"])}</h3><p>{e(w["desc"])}</p></a>'
        for w in C["works"]
    )
    news = "".join(
        f'<li><a href="#"><time>{e(n["date"])}</time><span class="cat">{e(n["cat"])}</span><span>{e(n["title"])}</span></a></li>'
        for n in C["news"]
    )
    links = "".join(f'<li><a href="{e(x["url"])}">{e(x["label"])}</a></li>' for x in C["links"])
    n0 = C["news"][0]
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(C["name_en"])} | Portfolio</title>
<meta name="description" content="{e(C["about"])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{t["gf"]}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head>
<body>
<div class="util"><div class="wrap"><a href="#news">お知らせ</a><a href="#contact">お問い合わせ</a><a href="../">デザイン一覧</a></div></div>
<header class="gh"><div class="wrap"><a class="logo" href="#"><i></i>{e(C["name_en"])}</a>
<nav class="gnav"><a href="#services">サービス</a><a href="#about">プロフィール</a><a href="#works">実績</a><a href="#news">お知らせ</a></nav>
<a class="btn btn-primary" href="#contact">お問い合わせ</a></div></header>
<section class="hero"><div class="wrap"><div><p class="eyebrow">{e(t["eyebrow"])}</p><h1>{e(t["hero"])}</h1>
<p class="lead">{e(t["lead"])}</p><div class="cta"><a class="btn btn-primary" href="#works">実績を見る</a><a class="btn btn-ghost" href="#contact">相談する</a></div></div>
<div class="visual" aria-hidden="true"><span></span><span></span><span></span></div></div></section>
<div class="notice"><div class="wrap"><b>NEWS</b><time>{e(n0["date"])}</time><a href="#news">{e(n0["title"])}</a></div></div>
<section class="sec"><div class="wrap"><div class="stats">{stats}</div></div></section>
<section class="sec" id="services"><div class="wrap"><div class="sec-head"><div><span class="en">SERVICES</span><h2>提供できること</h2></div></div><div class="services">{svcs}</div></div></section>
<section class="sec about" id="about"><div class="wrap"><div class="about-vis reveal" aria-hidden="true"></div><div class="reveal">
<div class="sec-head"><div><span class="en">PROFILE</span><h2>{e(C["name"])}</h2></div></div><p>{e(C["about"])}</p><ul class="skills">{skills}</ul></div></div></section>
<section class="sec" id="works"><div class="wrap"><div class="sec-head"><div><span class="en">WORKS</span><h2>実績紹介</h2></div><a class="more" href="#">すべての実績</a></div><div class="works">{works}</div></div></section>
<section class="sec" id="news"><div class="wrap"><div class="sec-head"><div><span class="en">NEWS</span><h2>お知らせ</h2></div><a class="more" href="#">一覧を見る</a></div><ul class="news">{news}</ul></div></section>
<section class="ctaband" id="contact"><div class="wrap"><div><h2>お仕事のご相談はこちらから</h2><p>内容が固まっていなくても大丈夫です。お気軽にご連絡ください。</p></div>
<a class="btn btn-primary" href="mailto:{e(C["email"])}">お問い合わせ</a></div></section>
<footer class="gf"><div class="wrap"><div class="cols"><div><a class="logo" href="#"><i></i>{e(C["name_en"])}</a><p style="margin-top:16px;opacity:.7">{e(C["role"])}</p></div>
<div><h4>サービス</h4><ul>{"".join(f'<li><a href="#services">{e(s["title"])}</a></li>' for s in C["services"])}</ul></div>
<div><h4>サイト</h4><ul><li><a href="#about">プロフィール</a></li><li><a href="#works">実績</a></li><li><a href="#news">お知らせ</a></li></ul></div>
<div><h4>SNS</h4><ul>{links}</ul></div></div>
<div class="copy"><span>© 2026 {e(C["name_en"])}. All rights reserved.</span><a href="../">← デザイン一覧へ</a></div></div></footer>
<script>
const io=new IntersectionObserver(es=>es.forEach(x=>{{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target)}}}}),{{threshold:.15}});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
</script>
</body></html>
"""


def index():
    cards = ""
    for t in THEMES:
        sw = "".join(f'<span class="chip" style="background:{h}" title="{e(n)} {h}"></span>' for n, h in t["colors"])
        codes = " / ".join(h for _, h in t["colors"])
        kw = "".join(f"<span>#{e(k)}</span>" for k in t["keywords"])
        bg, fg = t["head"]
        cards += f"""<a class="tm" href="{t["id"]}/">
<div class="tm-head" style="background:{bg};color:{fg}"><span>{t["id"][:2]}</span><h2>{e(t["name"])}</h2><p>{e(t["jp"])}</p></div>
<div class="tm-body"><p class="ind">想定業種：{e(t["industry"])}</p><p class="ref">参考にした雰囲気：{e(t["ref"])}</p><p>{e(t["concept"])}</p>
<div class="kw">{kw}</div><div class="sw">{sw}</div><p class="meta">{codes}<br>見出し {e(t["fonts"][0])} ／ 本文 {e(t["fonts"][1])}</p>
<span class="go">サイトを見る →</span></div></a>"""
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Portfolio Design Patterns</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}a{{color:inherit;text-decoration:none}}
body{{font-family:'Inter','Noto Sans JP',sans-serif;background:#f5f5f7;color:#1d1d1f;line-height:1.7}}
header,main{{max-width:1240px;margin:0 auto;padding:0 32px}}
header{{padding-top:72px;padding-bottom:40px}}header small{{letter-spacing:.2em;color:#6e6e73;font-weight:700}}
header h1{{font-size:clamp(30px,4vw,48px);margin:8px 0}}header p{{color:#6e6e73}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:24px;padding-bottom:96px}}
.tm{{background:#fff;border-radius:20px;overflow:hidden;display:flex;flex-direction:column;transition:transform .25s,box-shadow .25s}}
.tm:hover{{transform:translateY(-4px);box-shadow:0 20px 40px rgba(0,0,0,.08)}}
.tm-head{{padding:32px 28px;min-height:160px}}.tm-head span{{font-size:12px;opacity:.7}}.tm-head h2{{font-size:28px;line-height:1.2;margin-top:24px}}.tm-head p{{opacity:.8;font-size:14px}}
.tm-body{{padding:24px 28px 28px;display:flex;flex-direction:column;gap:14px;flex:1;font-size:14px}}
.ind{{font-weight:700;font-size:13px}}.ref{{font-size:12px;color:#6e6e73;margin-top:-10px}}
.kw span{{display:inline-block;background:#f5f5f7;border-radius:999px;padding:2px 10px;margin:0 6px 6px 0;font-size:12px}}
.sw{{display:flex;gap:6px}}.chip{{width:32px;height:32px;border-radius:8px;border:1px solid rgba(0,0,0,.1)}}
.meta{{font-size:12px;color:#6e6e73}}.go{{margin-top:auto;font-weight:700;color:#0066cc}}
@media (max-width:640px){{header,main{{padding-left:16px;padding-right:16px}}main{{grid-template-columns:1fr}}}}
</style></head><body>
<header><small>DESIGN PATTERNS</small><h1>5業種・5カラーのデザインパターン</h1><p>業種や色の系統がまったく違う5つのサイトを、同じ内容で設計しました。ご依頼のブランドに合わせて、どのテイストでも制作できます。</p></header>
<main>{cards}</main></body></html>
"""


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(index(), encoding="utf-8")
    for t in THEMES:
        d = OUT / t["id"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page(t), encoding="utf-8")
        (d / "style.css").write_text(BASE_CSS + t["css"], encoding="utf-8")
    print("built", len(THEMES), "pro patterns")


if __name__ == "__main__":
    main()
