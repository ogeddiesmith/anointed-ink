#!/usr/bin/env python3
"""
Build gate for anointedink.

Nestor's advertising is wired to his Illinois body art establishment registration:
A conviction for false or deceptive advertising is a ground to suspend or revoke it (77 Ill.
Adm. Code 797.1600(b)); any violation of the Act or Part 797 carries up to $1,000 for each day
the registrant remains in violation (797.1700(b)); and the claims are reachable directly under
815 ILCS 510. So this is a gate, not a checklist.

  python3 lint.py      exit 0 = clean, exit 1 = do not ship
"""
import glob, html, json, os, re, sys

FAIL = []
WARN = []

# ---------------------------------------------------------------- banned terms
# Grouped by the rule each one breaks. See ../CLIENT-BRIEF.md for citations.
CREDENTIAL = [  # 815 ILCS 510/2(a)(5). Illinois licenses ESTABLISHMENTS, not artists,
                # so "licensed tattoo artist" names a credential that does not exist.
    "licensed", "certified", "board-certified", "state-certified", "accredited",
    "credentialed", "award-winning", "award winning", "voted best", "top-rated",
    "top rated", "premier", "industry-leading",
]
HEALTH = [  # FTC 16 CFR 255.2(a) substantiation; IDPH routes health questions to physicians
    "heals", "healing", "will heal", "healed perfectly", "risk-free", "risk free",
    "sterile", "sterilized", "medical-grade", "medical grade", "hospital-grade",
    "hospital grade", "infection-free", "hypoallergenic", "non-toxic", "nontoxic",
    "scar-free", "no scarring", "fda-approved", "fda approved",
]
PAIN = [  # FDA March 2024 warning letters to tattoo numbing sellers
    "painless", "pain-free", "pain free", "numbing", "virtually painless",
]
SUPERIORITY = [  # 815 ILCS 510/2(a)(7). Four named local rivals have a private right of action.
    "best in chicago", "best in the suburbs", "best tattoo shop", "cleanest shop",
    "safest shop", "most experienced", "better than any", "#1 in",
]
AFTERCARE = [  # 797.600(b)-(c): verbal + written aftercare in the shop. Off the web by choice
    "aftercare instructions", "how to care for your tattoo", "aftercare guide",
]
BANNED = [(t, "credential") for t in CREDENTIAL] + [(t, "health") for t in HEALTH] + \
         [(t, "pain") for t in PAIN] + [(t, "superiority") for t in SUPERIORITY] + \
         [(t, "aftercare") for t in AFTERCARE]

# Phrases that are legal to say only in the negative, eg "we do not offer numbing".
ALLOWED_CONTEXT = re.compile(r"(do not|does not|never|no |without |cannot|can't)\s*\w*\s*$", re.I)

STOCK = ["unsplash", "pexels", "shutterstock", "istockphoto", "gettyimages", "freepik"]
UK = ["colour", "centre", "organise", "recognise", "specialis", "favourite", "honours",
      "stencilled", "stencilling", "travelled", "jewellery", "cancelled", "labelled", "modelled"]

# Aftercare slips in as a one-line imperative, not as a heading. 2026-09-24 a blog post shipped
# "Keep the piece covered when you are out in it", which no term above catches (797.600).
CARE_IMPERATIVE = re.compile(
    r"\bkeep (it|the piece|the tattoo|your tattoo|your new tattoo) "
    r"(covered|out of the sun|moisturi[sz]ed|clean|wrapped)\b"
    r"|\b(sunscreen|sunblock|spf ?\d+)\b|\bmoisturi[sz]e\b|\b(do not|don't|never) (swim|soak)\b", re.I)
# Things the artist must not promise or prescribe. Warn, then a human reads the sentence.
PROMISE = re.compile(r"\b(in|after) (twenty|thirty|\d+) years\b|\bhow many (laser )?sessions\b"
                     r"|\bguarantee", re.I)


def check_text(path, text):
    low = text.lower()
    for term, kind in BANNED:
        for m in re.finditer(re.escape(term), low):
            before = low[max(0, m.start() - 40):m.start()]
            if ALLOWED_CONTEXT.search(before):
                WARN.append(f"{path}: '{term}' ({kind}) appears in a negated sentence, verify")
                continue
            ctx = text[max(0, m.start() - 55):m.start() + len(term) + 45].replace("\n", " ")
            FAIL.append(f"{path}: BANNED [{kind}] '{term}'  ...{ctx}...")
    if "—" in text or "&mdash;" in text:
        FAIL.append(f"{path}: em dash present ({text.count(chr(8212)) + text.count('&mdash;')}x)")
    for u in UK:
        if u in low:
            FAIL.append(f"{path}: UK spelling '{u}'")
    for sdk in STOCK:
        if sdk in low:
            FAIL.append(f"{path}: stock photo source '{sdk}'")
    for m in CARE_IMPERATIVE.finditer(text):
        ctx = text[max(0, m.start() - 55):m.end() + 45].replace("\n", " ")
        FAIL.append(f"{path}: aftercare instruction '{m.group(0)}'  ...{ctx}...")
    for m in PROMISE.finditer(text):
        ctx = text[max(0, m.start() - 55):m.end() + 45].replace("\n", " ")
        WARN.append(f"{path}: promise or prescription, read it: '{m.group(0)}'  ...{ctx}...")
    if re.search(r"18\s*\+?\s*(or|,)?\s*(with|unless)\s+(a\s+)?parent", low):
        FAIL.append(f"{path}: implies parental consent can authorize tattooing a minor. "
                    "Illinois has no such exception (720 ILCS 5/12C-35).")


def main():
    pages = sorted(glob.glob("**/*.html", recursive=True))
    if not pages:
        print("no pages built"); return 1
    for p in pages:
        s = open(p).read()
        check_text(p, s)

        # one h1, present
        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        if len(h1) != 1:
            FAIL.append(f"{p}: {len(h1)} h1 tags, expected exactly 1")

        # title and description within range
        t = re.search(r"<title>(.*?)</title>", s)
        d = re.search(r'name="description" content="(.*?)"', s)
        if not t or not d:
            FAIL.append(f"{p}: missing title or meta description")
        else:
            if len(t.group(1)) > 62: WARN.append(f"{p}: title {len(t.group(1))} chars")
            if len(d.group(1)) > 158: WARN.append(f"{p}: description {len(d.group(1))} chars")

        # every img needs alt, width, height
        for img in re.findall(r"<img\b[^>]*>", s):
            if 'alt="' not in img:
                FAIL.append(f"{p}: <img> without alt: {img[:90]}")
            elif 'alt=""' in img and "lb" not in p:
                pass  # the lightbox img is populated by JS
            if "width=" not in img or "height=" not in img:
                if 'src=""' not in img:
                    WARN.append(f"{p}: <img> without width/height: {img[:80]}")

        # JSON-LD must parse, and must never carry a self-serving rating
        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                obj = json.loads(blk)
            except Exception as e:
                FAIL.append(f"{p}: invalid JSON-LD: {e}"); continue
            flat = json.dumps(obj)
            if "aggregateRating" in flat or '"review"' in flat:
                FAIL.append(f"{p}: JSON-LD carries aggregateRating/review. Google's self-serving "
                            "review policy makes this ineligible and risks a manual action.")
        if "<html lang=" not in s:
            FAIL.append(f"{p}: missing lang attribute")
        if 'name="viewport"' not in s:
            FAIL.append(f"{p}: missing viewport meta")

    # manifest alt text sanity
    if os.path.exists("img/manifest.json"):
        for m in json.load(open("img/manifest.json")):
            if len(m["alt"]) < 20:
                WARN.append(f"manifest: thin alt text on {m['slug']}")
            check_text(f"manifest:{m['slug']}", m["alt"] + " " + m.get("caption", ""))

    print(f"checked {len(pages)} pages")
    for w in WARN[:25]:
        print("  WARN ", w)
    if len(WARN) > 25:
        print(f"  ... and {len(WARN)-25} more warnings")
    for f in FAIL:
        print("  FAIL ", f)
    print()
    if FAIL:
        print(f"RESULT: {len(FAIL)} FAILURES, {len(WARN)} warnings. DO NOT SHIP.")
        return 1
    print(f"RESULT: PASS. 0 failures, {len(WARN)} warnings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
