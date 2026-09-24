# -*- coding: utf-8 -*-
"""Page shell: head, nav, footer, schema, and the image helpers."""
import html, json, re
from _data import *
from _css import CSS
from _js import JS

MAN = json.load(open("img/manifest.json"))
BYSLUG = {m["slug"]: m for m in MAN}


def rel(path):
    """Relative prefix from a page at `path` back to the site root."""
    depth = path.count("/")
    return "../" * depth if depth else ""


def pic(slug, width, p="", cls="", lazy=True, sizes=None, w=None, h=None):
    """<picture> with AVIF then WebP then a JPEG fallback at 400."""
    m = BYSLUG[slug]
    sw, sh = m["sizes"][str(width)]
    if w and h:
        sw, sh = w, h
    r = rel(p)
    load = ('loading="lazy" decoding="async"' if lazy
            else 'fetchpriority="high" decoding="async"')
    sz = f' sizes="{sizes}"' if sizes else ""
    fb = f"{r}img/{slug}-400.jpg"
    return (f'<picture>'
            f'<source type="image/avif" srcset="{r}img/{slug}-{width}.avif"{sz}>'
            f'<source type="image/webp" srcset="{r}img/{slug}-{width}.webp"{sz}>'
            f'<img src="{fb}" alt="{html.escape(m["alt"])}" width="{sw}" height="{sh}" '
            f'{load}{" class=" + cls if cls else ""}></picture>')


def figure(slug, p="", tag_attrs=True, eager=False):
    """A gallery figure wired for the filter and the lightbox."""
    m = BYSLUG[slug]
    r = rel(p)
    fw, fh = m["sizes"]["1000"]
    attrs = ""
    if tag_attrs:
        attrs = (f' data-styles="{" ".join(m["styles"])}"'
                 f' data-full="{r}img/{slug}-1000.webp"'
                 f' data-fw="{fw}" data-fh="{fh}"'
                 f' data-alt="{html.escape(m["alt"], quote=True)}"'
                 f' data-caption="{html.escape(m["caption"], quote=True)}"')
    cap = f'<figcaption>{html.escape(m["caption"])}</figcaption>' if m.get("caption") else ""
    return f'<figure{attrs} tabindex="0">{pic(slug, 400, p, lazy=not eager)}{cap}</figure>'


def by_tags(tags, limit=None, exclude=()):
    """Manifest entries carrying any of `tags`, best first."""
    out = [m for m in MAN
           if any(t in m["styles"] for t in tags) and m["slug"] not in exclude]
    return out[:limit] if limit else out


# --------------------------------------------------------------------- schema
def shop_ld():
    return {
        "@context": "https://schema.org", "@type": ["TattooParlor", "LocalBusiness"],
        "@id": BASE + "/#shop",
        "name": BIZ,
        "description": (f"Custom tattoo shop in {CITY}, {STATE_FULL}. Black and grey Chicano "
                        f"realism, portraits, color realism, memorials, cover-ups and custom "
                        f"work by {ARTIST}."),
        "url": BASE + "/", "telephone": PHONE, "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
                    "addressRegion": STATE, "postalCode": ZIP, "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
        "hasMap": GBP, "priceRange": "$$", "currenciesAccepted": "USD",
        "image": [f"{BASE}/img/{m['slug']}-1000.webp" for m in MAN[:6]],
        "logo": f"{BASE}/img/og.jpg",
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": f"https://schema.org/{d}",
             "opens": o, "closes": c} for d, o, c in HOURS] + [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": "https://schema.org/Sunday", "opens": "00:00", "closes": "00:00"}],
        "sameAs": [IG, FB, FBPAGE, SNAP],
        "areaServed": [{"@type": "City", "name": a} for a in AREAS if "'" not in a],
        "founder": {"@type": "Person", "@id": BASE + "/about/#nestor", "name": ARTIST,
                    "alternateName": HANDLE, "jobTitle": "Owner and Tattoo Artist"},
        "knowsAbout": ["Black and grey Chicano realism", "Portrait tattoos", "Cover-up tattoos",
                       "Color realism tattoos", "Memorial tattoos", "Aztec and cultural tattoos",
                       "Religious tattoos"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Tattoo services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {
                    "@type": "Service",
                    "name": re.sub("<[^>]+>", "", sp["h1"]).replace("&amp;", "and"),
                    "url": f"{BASE}/{sp['slug']}/"}} for sp in STYLE_PAGES]},
        # aggregateRating and review are deliberately absent. Under Google's self-serving
        # review policy a business marking up its own reviews is INELIGIBLE for the star
        # feature, so the markup buys nothing and the only outcomes are neutral or bad.
        # (Verified 2026-09-24: this is an eligibility rule, not an automatic penalty. The
        # manual-action risk attaches to marking up content that is not visible on the page.)
        # The 5.0 from 115 is shown as visible, dated, linked body text instead.
    }


def breadcrumbs(trail, path):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
    for i, (name, href) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": name,
                      "item": f"{BASE}/{href}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


# ----------------------------------------------------------------- head/foot
def head(title, desc, path, extra_ld=None, og_img="og", preload=None, crumbs=None,
         extra_head="", lang="en"):
    robots = ("index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
              if INDEXABLE else "noindex,nofollow")
    canon = f"{BASE}/{path}" if path else BASE + "/"
    r = rel(path)
    ld = [shop_ld()]
    if crumbs:
        ld.append(breadcrumbs(crumbs, path))
    if extra_ld:
        ld.extend(extra_ld)
    blocks = "\n".join('<script type="application/ld+json">' +
                       json.dumps(x, ensure_ascii=False, separators=(",", ":")) + "</script>"
                       for x in ld)
    links = "".join(
        f'<a href="{r}{h}"{" aria-current=page" if h == path else ""}>{t}</a>'
        for h, t in NAV)
    pl = ""
    if preload:
        pl = (f'<link rel="preload" as="image" href="{r}img/{preload}-1000.avif" '
              f'type="image/avif" fetchpriority="high">')
    ogimg = f"{BASE}/img/og.jpg" if og_img == "og" else f"{BASE}/img/{og_img}-1000.webp"
    ogw, ogh = (1200, 630) if og_img == "og" else BYSLUG[og_img]["sizes"]["1000"]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BIZ}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="{ogw}">
<meta property="og:image:height" content="{ogh}">
<meta property="og:image:alt" content="{BIZ}, custom tattoos by {ARTIST} in {CITY}, {STATE}">
<meta property="og:locale" content="{lang}_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{ogimg}">
<meta name="theme-color" content="#08080a">
<meta name="geo.region" content="US-IL">
<meta name="geo.placename" content="{CITY}">
<meta name="geo.position" content="{LAT};{LNG}">
<meta name="ICBM" content="{LAT}, {LNG}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%2308080a'/><text x='16' y='23' font-size='19' font-family='Helvetica' font-weight='bold' fill='%23c9a24a' text-anchor='middle'>A</text></svg>">
<link rel="apple-touch-icon" href="{BASE}/img/og.jpg">
{pl}{extra_head}
<style>{CSS}</style>
{blocks}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header><div class="wrap nav">
<a class="brand" href="{r or "./"}">Anointed <span>Ink</span></a>
<nav class="navlinks" aria-label="Main">{links}</nav>
<a class="callbtn" href="tel:{TEL}">Call {PHONE}</a>
<button class="burger" aria-label="Menu" aria-expanded="false">&#9776;</button>
</div></header>
<main id="main">"""


def hours_table():
    rows = "".join(f"<tr><th>{d}</th><td>12:00pm to 7:00pm</td></tr>" for d, _, _ in HOURS)
    return (f'<table class="hrs"><caption class="sr">Opening hours</caption><tbody>{rows}'
            f"<tr><th>Sunday</th><td>Closed</td></tr></tbody></table>")


def visit(path="", h2="Visit the shop"):
    return f"""<section id="visit" class="alt"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Find us</p><h2>{h2}</h2>
<p>We are on 111th Street in {CITY}, minutes from Oak Lawn, Worth, Alsip and Burbank.</p></div>
<div class="visit">
 <div>
  <address class="addr"><strong>{BIZ}</strong><br>{STREET}<br>{CITY}, {STATE} {ZIP}<br>
   <a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></address>
  <p style="margin-top:20px"><a class="btn btn-s" href="{GBP}" rel="noopener">Get directions</a></p>
  <p class="areas" style="margin-top:24px"><strong style="color:var(--tx)">Serving</strong><br>
  {", ".join(AREAS)}.</p>
 </div>
 <div><h3>Hours</h3>{hours_table()}
  <p class="areas" style="margin-top:20px">Plus code {PLUSCODE}</p></div>
</div></div></section>"""


def lightbox():
    return """<div class="lb" aria-hidden="true" role="dialog" aria-label="Tattoo photograph">
<button class="x" aria-label="Close">&times;</button>
<button class="prev" aria-label="Previous">&#8249;</button>
<button class="next" aria-label="Next">&#8250;</button>
<figure><img src="" alt=""><figcaption></figcaption></figure></div>"""


def foot(path=""):
    r = rel(path)
    pages = "".join(f'<li><a href="{r}{h}">{t}</a></li>' for h, t in NAV)
    styles = "".join(f'<li><a href="{r}{s["slug"]}/">{s["nav"]}</a></li>' for s in STYLE_PAGES[:6])
    return f"""</main>
<footer><div class="wrap"><div class="foot">
 <div>
  <h3>{BIZ}</h3>
  <p>Custom tattooing by {ARTIST} in {CITY}, {STATE_FULL}.<br>
  Black &amp; grey Chicano realism, portraits, color, memorials and cover-ups.</p>
  <p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p><a href="{IG}" rel="noopener me">Instagram</a> &middot;
     <a href="{FB}" rel="noopener me">Facebook</a> &middot;
     <a href="{GBP}" rel="noopener">Google</a></p>
 </div>
 <div><h3>Pages</h3><ul>{pages}</ul></div>
 <div><h3>Work</h3><ul>{styles}</ul></div>
 <div><h3>Visit</h3><ul>
   <li>{STREET}</li><li>{CITY}, {STATE} {ZIP}</li>
   <li>Mon to Sat, 12pm to 7pm</li><li>Sunday closed</li>
   <li><a href="{GBP}" rel="noopener">Directions</a></li></ul></div>
</div>
<div class="legal">&copy; 2026 {BIZ}. Every tattoo photograph on this site is
{ARTIST}&rsquo;s own work.</div>
</div></footer>
<div class="stickybar">
 <a class="btn-p" href="{SMS}" style="background:var(--gold);color:#14100a">Text your idea</a>
 <a class="btn-s" href="tel:{TEL}" style="border:1px solid var(--line2);color:var(--tx);background:var(--surface)">Call</a>
</div>
<script>{JS}</script>
</body></html>"""
