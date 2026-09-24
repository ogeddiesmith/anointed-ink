# Anointed Ink

Static marketing site for **Anointed Ink**, the tattoo shop owned by **Nestor Juarez**
(`Tat2Nestuhh`) at 5920 W 111th St, Chicago Ridge, IL 60415.

Live preview: https://ogeddiesmith.github.io/anointed-ink/

Built by [Simply Digital](https://simplydigitalmarketing.co).

---

## Status: preview, not launched

The site ships **`noindex`** with `Disallow: /` in robots.txt. It names a real business with a
real phone number, and Nestor has not signed off on the copy yet.

Two switches in `_data.py` take it live:

```python
INDEXABLE = False   # -> True once the copy is approved
BASE = "https://ogeddiesmith.github.io/anointed-ink"   # -> the real domain
```

`anointedink.com` and `.net` are both taken by an unrelated screen printing business.

## Build

```bash
python3 build.py     # writes the static site into this directory
python3 lint.py      # compliance + SEO gate. exit 1 means do not ship.
python3 make-og.py tattoo-catrina-woman-with-roses   # regenerate the 1200x630 social card
```

Photo assets are generated separately, from the raw originals kept outside this repo:

```bash
cd ../photos && python3 process.py
```

## Layout

| File | What it is |
|---|---|
| `_data.py` | Every verified fact: NAP, hours, rate, reviews, style pages, nav. Sources in the client brief. |
| `_css.py` | The design system. One string, inlined into every page. |
| `_js.py` | Gallery filtering, lightbox, mobile nav. No dependencies. |
| `_shell.py` | Page head, nav, footer, schema, responsive image helpers. |
| `build.py` | Page content and the emitter. |
| `lint.py` | The build gate (see below). |
| `img/manifest.json` | Per-photo metadata: alt text, style tags, dimensions, quality rank. |

## Why `lint.py` exists

Nestor's advertising is wired to his Illinois body art establishment registration.
A conviction for false or deceptive advertising is a ground to suspend or revoke that
registration (77 Ill. Adm. Code 797.1600(b)), and any violation of the Act or Part 797 carries a
fine of up to $1,000 **for each day** the registrant remains in violation (797.1700(b)). The
claims are also reachable directly under 815 ILCS 510. (Corrected 2026-09-24 against the rule
text: this used to say 797.1600(b) needs no conviction and that the fine runs each day a page is
up.)

So the linter is a gate, not a checklist. It fails the build on:

- **Credential claims** (`licensed`, `certified`, `award-winning`). Illinois registers
  establishments, not individual artists, so "licensed tattoo artist" names a credential that
  does not exist in this state.
- **Health, pain and numbing language.** The FDA issued warning letters to tattoo numbing
  sellers in March 2024.
- **Superiority claims.** Four named local rivals have a private right of action under
  815 ILCS 510/2(a)(7).
- **Aftercare content, by choice.** 77 Ill. Adm. Code 797.600(b) requires verbal and written
  aftercare instructions for each client, and 797.600(c) signed Department education materials.
  Nothing bans aftercare online; the site keeps it off so it never contradicts the in-shop duty.
  (Corrected 2026-09-24: this used to say the rule requires state forms signed by both parties.)
- **"18+ with parental consent" phrasing.** Illinois has no parental consent exception for
  tattooing (720 ILCS 5/12C-35(a)).
- `aggregateRating` in JSON-LD, em dashes, UK spellings, stock photo sources, missing alt
  text, invalid JSON-LD.

## Deliberate technical decisions

**No `aggregateRating` markup.** Under Google's self-serving review policy, a business marking
up reviews about itself is ineligible for the star feature, so the markup buys nothing. The
5.0 from 115 Google reviews is published as visible, **date-stamped**, linked body text instead.

**Every photograph is Nestor's own work.** No stock imagery, ever. On a tattoo site a stock
tattoo reads as the artist's portfolio. `lint.py` fails the build if a stock source appears.
