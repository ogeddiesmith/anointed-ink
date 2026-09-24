#!/usr/bin/env python3
"""
Render the 1200x630 social preview card.

og:image must be an absolute URL and a real JPEG, because social scrapers do not
run JS and several will not take WebP or AVIF. Run after build.py.
  python3 make-og.py <hero-slug>
"""
import json, os, subprocess, sys, base64

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = "img/og.jpg"

def main():
    man = json.load(open("img/manifest.json"))
    slug = sys.argv[1] if len(sys.argv) > 1 else man[0]["slug"]
    hero = next((m for m in man if m["slug"] == slug), man[0])
    data = base64.b64encode(open(f"img/{hero['slug']}-1000.webp", "rb").read()).decode()

    html = """<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;display:flex;background:#0a0a0c;color:#eceae6;
 font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;overflow:hidden}
.l{flex:1;padding:66px 54px;display:flex;flex-direction:column;justify-content:center}
.eyebrow{font-size:20px;font-weight:800;letter-spacing:.24em;color:#d4a548;margin-bottom:26px}
h1{font-size:62px;line-height:1.04;font-weight:800;letter-spacing:-.025em;margin-bottom:24px}
.sub{font-size:26px;color:#a29d96;line-height:1.45;margin-bottom:32px}
.meta{display:flex;gap:16px;align-items:center;font-size:22px;font-weight:700}
.pill{background:#17171c;border:1px solid #2b2b34;border-radius:999px;padding:11px 22px}
.stars{color:#d4a548;letter-spacing:.06em}
.r{width:452px;position:relative;flex-shrink:0}
.r img{width:100%;height:100%;object-fit:cover}
.r::after{content:"";position:absolute;inset:0;
 background:linear-gradient(90deg,#0a0a0c 0%,rgba(10,10,12,.35) 34%,transparent 100%)}
</style><body>
<div class="l">
 <div class="eyebrow">CHICAGO RIDGE, ILLINOIS</div>
 <h1>Anointed Ink</h1>
 <div class="sub">Custom tattoos by Nestor Juarez.<br>Black &amp; grey Chicano realism, portraits,
 cover-ups.</div>
 <div class="meta">
  <span class="pill"><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 5.0 &middot; 115 reviews</span>
  <span class="pill">(708) 770-2754</span>
 </div>
</div>
<div class="r"><img src="data:image/webp;base64,__IMG__"></div>
</body>""".replace("__IMG__", data)

    open("_og.html", "w").write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=1200,630",
                    "--screenshot=_og.png", "--virtual-time-budget=4000",
                    "file://" + os.path.abspath("_og.html")],
                   check=True, capture_output=True)
    from PIL import Image
    im = Image.open("_og.png").convert("RGB")
    im = im.resize((1200, 630), Image.LANCZOS)
    im.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
    os.remove("_og.png"); os.remove("_og.html")
    print(f"og image: {OUT}  {im.size}  {os.path.getsize(OUT)/1024:.0f}KB  hero={hero['slug']}")

if __name__ == "__main__":
    main()
