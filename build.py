# -*- coding: utf-8 -*-
"""
anointedink site builder.

  python3 build.py

Writes the static site into this directory. Every fact comes from _data.py and
every fact in there has a named source in ../CLIENT-BRIEF.md.
"""
import html, json, os, re, shutil
from _data import *
from _shell import (head, foot, visit, hours_table, lightbox, pic, figure, by_tags,
                    breadcrumbs, MAN, BYSLUG, rel)

PAGES = {}


def write(path, content):
    PAGES[path] = content


def trust_bar():
    return f"""<div class="trust"><div class="wrap trust-in">
 <span><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> <b>{GRATING}</b> from
  {GCOUNT} <a href="{GBP}" rel="noopener">Google reviews</a></span>
 <span><b>{RATE}/hour</b> shop rate</span>
 <span><b>18+</b> photo ID required</span>
 <span><b>{len(MAN)} pieces</b> in the gallery</span>
 <span><b>Mon to Sat</b> 12pm to 7pm</span>
</div></div>"""


def reviews_block(path=""):
    revs = "".join(
        f'<div class="rev"><blockquote>&ldquo;{q}&rdquo;</blockquote>'
        f"<cite>{who} &middot; Google review</cite></div>" for q, who in REVIEWS)
    return f"""<section><div class="wrap">
<div class="sec-head"><p class="eyebrow">Selected reviews from Google</p>
<h2>{GRATING} stars from {GCOUNT} reviews</h2>
<p>As of {RATING_AS_OF}. These three are a selection, quoted exactly as written, spelling and
all. <a href="{GBP}" rel="noopener">Read all {GCOUNT} on Google</a> rather than taking our pick
of them.</p></div>
<div class="grid g3">{revs}</div></div></section>"""


# ===================================================================== HOME
STYLE_CARDS = [
    ("Black &amp; grey Chicano realism",
     "Smooth grey wash, hard contrast, and the masks, script and religious imagery the style was "
     "built on. This is the work Nestor is asked for most.", "black-and-grey-chicano-realism/"),
    ("Cover-ups",
     "Old work, faded work, or a name you would rather not explain. Cover-ups are their own "
     "discipline and they need an artist who has done a lot of them.", "cover-up-tattoos/"),
    ("Portraits",
     "Faces in black and grey or color, worked up from a photograph you bring in. The hardest "
     "thing to get right and the first thing people notice.", "portrait-tattoos/"),
    ("Religious pieces",
     "Christ portraits, praying hands, crosses, scripture and cherubs. A large share of what "
     "comes through this shop, and the reason for the shop&rsquo;s name.", "religious-tattoos/"),
    ("Memorials",
     "Portraits, dates, script and the imagery that belongs with them, laid out so the piece "
     "still reads clearly twenty years from now.", "memorial-tattoos/"),
    ("Aztec &amp; cultural work",
     "Jaguar and eagle warriors, sun stones, headdresses and the heritage imagery that sits at "
     "the center of Chicano tattooing.", "aztec-and-chicano-culture-tattoos/"),
    ("Color realism",
     "Fully saturated work, packed and blended, for pieces meant to be seen from across a room.",
     "color-realism-tattoos/"),
    ("Sleeves",
     "Half and full sleeves planned as one composition and built over several sittings, rather "
     "than collected one patch at a time.", "tattoo-sleeves/"),
]

FAQ = [
    ("Do I need a deposit to book?",
     "Yes. A deposit holds your appointment and it comes off the price of the tattoo on the day. "
     "It pays for the drawing time that happens before you ever sit down, which is why it is "
     "asked for up front."),
    ("What does a tattoo cost here?",
     f"The shop rate is {RATE} an hour. What a given piece costs depends on size, placement and "
     "how much detail is in it, so the honest answer is to send a reference and get a quote. "
     "Smaller pieces are usually quoted as a flat price rather than hourly."),
    ("Do you do cover-ups?",
     "Yes, and they are a regular part of the work here. Send a clear, well lit photo of the "
     "existing tattoo before booking so the new design can be built around what is already "
     "there. Not every tattoo can be covered at any size, and you will be told that up front "
     "rather than halfway through."),
    ("Can I bring my own design?",
     "Bring references, photographs, or a rough idea on your phone. Most pieces start from "
     "something the client brings in and get drawn up from there. Custom drawing time is "
     "covered by the deposit."),
    ("How long will my tattoo take?",
     "You will be told how many sittings a piece needs before anything is booked, not after. A "
     "sleeve is planned as one composition and then built in stages, so you always know what is "
     "coming next."),
    ("How old do I have to be?",
     "Eighteen, and a parent cannot sign that away. Under 720 ILCS 5/12C-35(a) it is a Class A "
     "misdemeanor in Illinois to tattoo, or even to offer to tattoo, anyone under 18, and there "
     "is no parental consent exception in the tattoo statute. Different body art procedures are "
     "governed by different rules, but for tattooing the answer is simply no."),
    ("Do I need to bring ID?",
     "Yes, a government-issued photo ID showing your date of birth, every visit. Illinois rules "
     "require the shop to verify age from the ID itself (77 Ill. Adm. Code 797.400(k)), which "
     "means we check it even for people we have tattooed a dozen times."),
    ("Can I bring my kid with me to my appointment?",
     "Only with their parent or legal guardian physically present. 720 ILCS 5/12C-35(b) says a "
     "person under 18 may not enter or remain on the premises where tattooing is being performed "
     "unless accompanied by a parent or legal guardian. Note that this is an accompaniment rule, "
     "not a consent form: somebody has to actually be there with them. If you are the one in the "
     "chair and your child would otherwise be on their own, arrange childcare first."),
    ("Where are you located?",
     f"{STREET}, {CITY}, {STATE} {ZIP}, on 111th Street. Minutes from Oak Lawn, Worth, Alsip, "
     "Burbank and Evergreen Park, and an easy run from the southwest side of the city."),
]

STEPS = [
    ("Send your idea",
     f"Message {IG_HANDLE} on Instagram, message the shop on Facebook, or call {PHONE}. Send a "
     "reference image, roughly where on your body it goes, and a size."),
    ("Get a straight quote",
     "You will get a real answer on price and on how many sittings it takes before anything is "
     "booked. If the idea will not work at the size you want, you will hear that too."),
    ("Leave a deposit",
     "The deposit locks your date and covers the drawing time. It comes off the final price."),
    ("Come in and sit",
     "Bring photo ID. Eat beforehand. Plan for the session to run the length you were quoted."),
]


def build_home():
    cards = "".join(
        f'<a class="card" href="{href}"><h3>{t}</h3><p>{d}</p>'
        f'<span class="more">See the work &rarr;</span></a>' for t, d, href in STYLE_CARDS)
    feat = [m["slug"] for m in MAN if m["quality"] >= 4][:12]
    gal = "".join(figure(x, eager=(i < 6)) for i, x in enumerate(feat))
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": html.unescape(re.sub("<[^>]+>", "", q)),
         "acceptedAnswer": {"@type": "Answer",
                            "text": html.unescape(re.sub("<[^>]+>", "", a))}}
        for q, a in FAQ]}
    steps = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in STEPS)
    cov = BYSLUG.get("tattoo-crowned-skull-cover-up")

    return head(
        f"Tattoo Shop in {CITY}, IL | {BIZ}",
        f"Custom tattoos by {ARTIST} in {CITY}, IL. Black and grey Chicano realism, portraits, "
        f"cover-ups and memorials. {GRATING} stars from {GCOUNT} Google reviews.",
        "", extra_ld=[faq_ld], preload="tattoo-catrina-woman-with-roses") + f"""
<div class="hero"><div class="wrap hero-grid">
 <div>
  <p class="eyebrow">{BIZ} &middot; {CITY}, {STATE_FULL}</p>
  <h1>Custom tattoos for people who were never meant to blend in</h1>
  <p class="tagline">{TAGLINE}</p>
  <p class="lede">Black and grey Chicano realism, portraits, color, memorials, religious pieces
  and cover-ups, at {BIZ} on 111th Street. Every piece drawn for the person wearing it rather
  than pulled off a wall.</p>
  <p class="lede" style="margin-top:18px;color:var(--tx)">
   <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
   <strong>{GRATING} from {GCOUNT} Google reviews</strong>
   <span style="color:var(--muted2)"> as of {RATING_AS_OF}.</span>
   <a href="{GBP}" rel="noopener">Read them</a>.</p>
  <div class="cta">
   <a class="btn btn-p" href="{SMS}">Text your idea</a>
   <a class="btn btn-s" href="tel:{TEL}">Call {PHONE}</a>
   <a class="btn btn-s" href="gallery/">See {len(MAN)} tattoos</a>
  </div>
 </div>
 <div class="hero-img">{pic('tattoo-catrina-woman-with-roses', 1000, lazy=False,
                            sizes='(max-width:940px) 92vw, 46vw')}</div>
</div></div>

{trust_bar()}

<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">What we do</p>
 <h2>Every style, drawn from scratch</h2>
 <p>Nestor does not limit himself to one lane. The through line is custom work built around your
 idea, not a design that forty other people already have.</p></div>
 <div class="grid g4">{cards}</div>
</div></section>

<section class="alt"><div class="wrap">
 <div class="sec-head"><p class="eyebrow">Portfolio</p><h2>Recent work</h2>
 <p>Every photograph on this site is Nestor&rsquo;s own tattooing. Click any piece to see it
 larger.</p></div>
 <div class="gal-grid">{gal}</div>
 <p style="margin-top:28px"><a class="btn btn-s" href="gallery/">See all {len(MAN)} pieces
 &rarr;</a></p>
</div></section>

<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">Cover-ups</p>
 <h2>The tattoo you regret is not permanent</h2></div>
 <div class="grid g2" style="align-items:center">
  <div>
   <p>The photograph beside this is one job, shown twice. On the left is an old dark tattoo with
   the new design stencilled straight over the top of it. On the right is the finished piece.</p>
   <p>That is what a cover-up actually is. You are not erasing anything. You are designing a
   bigger, darker, busier piece whose shadows land exactly where the old ink sits, so the eye
   never finds it again.</p>
   <p>Send a clear daylight photo of what you have and you will get a straight answer on what is
   realistic, including when the answer is that it needs to be bigger than you hoped.</p>
   <p><a class="btn btn-p" href="cover-up-tattoos/">How cover-ups work &rarr;</a></p>
  </div>
  <div class="hero-img">{pic('tattoo-crowned-skull-cover-up', 1000,
                             sizes='(max-width:940px) 92vw, 46vw')}
   <p class="areas" style="padding:14px 4px 0;font-size:.87rem">Stencil over the existing tattoo,
   and the finished crowned skull. Same arm, same session.</p></div>
 </div>
</div></section>

{reviews_block()}

<section class="alt"><div class="wrap">
 <div class="sec-head"><p class="eyebrow">Booking</p><h2>How to get tattooed here</h2>
 <p>Serious inquiries only, and a deposit is required to hold a date. That is not gatekeeping,
 it is what protects your appointment and the drawing time that goes into it.</p></div>
 <ol class="steps">{steps}</ol>
 <div class="cta"><a class="btn btn-p" href="book/">Start a booking</a>
 <a class="btn btn-s" href="{IG}" rel="noopener me">Message on Instagram</a></div>
</div></section>

<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">Questions</p><h2>Before you book</h2></div>
 {faq}
</div></section>

{visit()}
{lightbox()}
""" + foot()


# ================================================================== GALLERY
def build_gallery():
    counts = {}
    for m in MAN:
        for s in m["styles"]:
            counts[s] = counts.get(s, 0) + 1
    order = [s for s, _ in sorted(counts.items(), key=lambda x: -x[1]) if counts[s] >= 2]
    chips = ('<button class="chip" data-filter="all" aria-pressed="true">All '
             f'{len(MAN)}</button>')
    chips += "".join(
        f'<button class="chip" data-filter="{s}" aria-pressed="false">'
        f'{STYLE_LABELS.get(s, s)} {counts[s]}</button>' for s in order)
    figs = "".join(figure(m["slug"], "gallery/", eager=(i < 6))
                   for i, m in enumerate(MAN))
    ld = {"@context": "https://schema.org", "@type": "ImageGallery",
          "name": f"Tattoo portfolio by {ARTIST}",
          "description": f"{len(MAN)} tattoos by {ARTIST} at {BIZ} in {CITY}, {STATE}.",
          "associatedMedia": [
              {"@type": "ImageObject", "contentUrl": f"{BASE}/img/{m['slug']}-1000.webp",
               "thumbnailUrl": f"{BASE}/img/{m['slug']}-400.webp",
               "caption": m["caption"], "creator": {"@id": BASE + "/about/#nestor"},
               "creditText": ARTIST, "license": BASE + "/"} for m in MAN]}
    return head(
        f"Tattoo Gallery | {len(MAN)} Tattoos by {ARTIST}",
        f"{len(MAN)} tattoos by {ARTIST} at {BIZ} in {CITY}, IL. Filter by black and grey "
        "realism, Chicano, portraits, color, Aztec, memorials and cover-ups.",
        "gallery/", extra_ld=[ld], crumbs=[("Gallery", "gallery/")],
        og_img="tattoo-catrina-woman-with-roses") + f"""
<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">Portfolio</p><h1>The gallery</h1>
 <p>{len(MAN)} tattoos, all of them Nestor&rsquo;s own work. Filter by style, and click any
 piece to open it full size.</p></div>
 <div class="filters" role="group" aria-label="Filter by style">{chips}</div>
 <p class="count">Showing {len(MAN)} pieces.</p>
 <div class="masonry">{figs}</div>
 <div class="note" style="margin-top:34px"><strong>About these photographs.</strong>
 Every image here is work Nestor tattooed himself. Several carry his own watermark, which reads
 <em>Ghtto_Mex</em> or <em>Tattoonestuh_Juarez</em>. Some pieces are photographed fresh, still
 under wrap, which is why the skin around them looks red.</div>
 <div class="cta"><a class="btn btn-p" href="tel:{TEL}">Call {PHONE}</a>
 <a class="btn btn-s" href="../book/">Book a consultation</a></div>
</div></section>
{visit("gallery/")}
{lightbox()}
""" + foot("gallery/")


# ============================================================== STYLE PAGES
STYLE_COPY = {
"black-and-grey-chicano-realism": dict(
 title="Chicano Black &amp; Grey Tattoos | {city}, IL",
 desc="Black and grey Chicano realism tattoos by {artist} in {city}, IL. Portraits, script, "
      "masks, religious and memorial work. Call {phone}.",
 lede="The style this shop is known for, tattooed in {city} and across the southwest suburbs.",
 body="""
<p>Black and grey is not a color tattoo with the color left out. It is built entirely from
contrast: how dark the darks go, how smooth the grey wash stays, and how much bare skin is left
doing nothing at all. Get that balance wrong and the piece turns into a grey smudge in five
years. Get it right and it still reads across a room in twenty.</p>
<p>Chicano tattooing layers its own vocabulary on top of that. Fine line script. Laugh now, cry
later masks. Catrinas and rosaries. Clocks, roses, and portraits of family. The lettering in
particular is unforgiving, because it is drawn freehand onto skin and a wobble is permanent.</p>
<p>Nestor has been tattooing for {years} years, and this is the work people drive out to
{city} for.</p>""",
 aside=("Portraits worked from your own photographs", "Fine line and Old English script",
        "Catrinas, masks and Day of the Dead imagery", "Religious pieces and memorial portraits",
        "Clocks, roses and traditional Chicano imagery", "Half and full sleeves built in stages")),

"cover-up-tattoos": dict(
 title="Cover-Up Tattoos in {city}, IL | {biz}",
 desc="Cover-up tattoos by {artist} in {city}, IL. Old or regretted work redrawn into "
      "something you want to show. Send a photo for a quote.",
 lede="Old work, faded work, a name you would rather not explain, or somebody else&rsquo;s "
      "mistake.",
 body="""
<p>A cover-up is a different problem from a fresh tattoo. You are not drawing on blank skin. You
are designing around something that is already there and is not going anywhere, and the new piece
has to be bigger, darker and busier in exactly the right places.</p>
<p>Which is why the first step is always a photograph. Send a clear, well lit picture of the
existing tattoo before booking anything. From that you get a straight answer on what is realistic,
including the answers people do not want: that it needs to be larger than you hoped, that it needs
a session of laser fading first, or that the design you have in mind is too light to do the job.</p>
<p>You will not be told a cover-up will work when it will not. That conversation is cheaper before
the needle than after it.</p>""",
 aside=("A clear photo in daylight, no flash", "A rough measurement of the existing tattoo",
        "What you would like to see there instead", "Whether it has been lasered or faded already",
        "Whether you are open to going larger")),

"portrait-tattoos": dict(
 title="Portrait Tattoos in {city}, IL | {artist}",
 desc="Portrait tattoos by {artist} in {city}, IL. Family, memorial and character "
      "portraits in black and grey or color.",
 lede="The hardest thing to get right, and the first thing anybody notices.",
 body="""
<p>A portrait is the least forgiving tattoo there is. Everybody looking at it already knows what a
face is supposed to do, so a millimetre of error in an eyelid reads instantly as wrong, even to
someone who has never thought about tattooing in their life.</p>
<p>The work starts with your photograph. A sharp, well lit, straight-on reference makes a good
portrait possible. A dark, low resolution phone picture with a hand across half the face does not,
and no amount of skill at the machine fixes a reference that never had the information in it.</p>
<p>Bring the best photo you have and you will hear honestly whether it is enough to work from.</p>""",
 aside=("Family and memorial portraits", "Religious portraits",
        "Character and film portraits", "Black and grey or full color",
        "Worked from your own reference photograph")),

"religious-tattoos": dict(
 title="Religious Tattoos in {city}, IL | {biz}",
 desc="Religious tattoos by {artist} in {city}, IL. Christ portraits, praying hands, crosses, "
      "cherubs and scripture in black and grey realism.",
 lede="Christ portraits, praying hands, crosses, cherubs and scripture.",
 body="""
<p>The shop is not called Anointed Ink by accident. A large share of the work that comes through
the door is faith-led, and Nestor takes that work seriously rather than treating it as one more
flash sheet.</p>
<p>Religious pieces tend to be the ones people think about the longest before booking, and they
are often the ones that carry the most weight afterwards. A Christ portrait on a shoulder, a
rosary down a forearm, a verse in script that only means something to the person wearing it.</p>
<p>These pieces also make the hardest technical demands, because a face in soft grey wash and a
tight line of script sitting beside each other need completely different handling.</p>""",
 aside=("Christ portraits", "Praying hands and rosaries", "Crosses and crucifixes",
        "Cherubs and angels", "Scripture and verse in script", "Guadalupe and saint imagery")),

"memorial-tattoos": dict(
 title="Memorial Tattoos in {city}, IL | {artist}",
 desc="Memorial tattoos by {artist} in {city}, IL. Portraits, dates, script and imagery laid "
      "out so the piece still reads clearly in twenty years.",
 lede="A piece you will carry for the rest of your life, so it gets planned properly.",
 body="""
<p>A memorial tattoo is the one piece nobody wants to redo. That changes how it should be
designed: bigger than you think, with more space around the elements than feels necessary on the
day, because fine detail and tight script are exactly what soften first.</p>
<p>Most memorial pieces combine a portrait, a date, and imagery that meant something to the
person. Getting those three to sit together as one composition rather than three tattoos in the
same place is most of the job.</p>
<p>There is no rush on these. Come in, talk it through, and let the drawing take the time it
takes.</p>""",
 aside=("Portraits worked from a photograph", "Dates in Roman numerals or script",
        "Handprints and signatures", "Doves, cherubs and wings",
        "Pieces built to stay readable as they age")),

"aztec-and-chicano-culture-tattoos": dict(
 title="Aztec Tattoos in {city}, IL | {biz}",
 desc="Aztec and cultural tattoos by {artist} in {city}, IL. Jaguar and eagle warriors, "
      "sun stones and headdresses, in black and grey or color.",
 lede="Warriors, sun stones, headdresses, and the heritage imagery at the center of Chicano "
      "tattooing.",
 body="""
<p>Aztec imagery is some of the most rewarding work to tattoo and some of the easiest to do badly.
The stonework has actual geometry in it. A sun stone with its rings out of true, or a warrior
headdress where the feather spacing has been guessed, looks wrong to anyone who knows the
reference, which in this neighborhood is a lot of people.</p>
<p>These are heritage pieces. They usually mean something specific to the person wearing them, and
they are worth getting right rather than approximating from the first image on a search results
page.</p>
<p>Bring what the piece needs to say and it gets drawn around that.</p>""",
 aside=("Jaguar and eagle warriors", "The sun stone and calendar imagery",
        "Headdresses and feather work", "Warrior and princess compositions",
        "Tribal banding and negative space work")),

"color-realism-tattoos": dict(
 title="Color Realism Tattoos in {city}, IL | {artist}",
 desc="Color realism tattoos by {artist} in {city}, IL. Saturated, packed and blended work in "
      "animals, florals and portraits.",
 lede="Fully saturated work, for pieces meant to be seen from across a room.",
 body="""
<p>Color realism asks for a different discipline than black and grey. The blends have to be packed
properly or they go patchy, the palette has to be decided before the first line goes in, and the
piece has to be designed to survive the way color settles over the first year.</p>
<p>Some pieces are better in color and some are not, and you will get an honest opinion on which
yours is. A portrait usually wants black and grey. A jaguar warrior headdress, a tiger, or a
sleeve of lilies usually wants color.</p>
<p>Plenty of the work here is both: a black and grey composition with one element carrying all the
color, which is often the strongest version of the idea.</p>""",
 aside=("Animals and wildlife", "Florals and botanical work",
        "Aztec and cultural pieces in full color",
        "Selective color over a black and grey base", "Character and anime work")),

"tattoo-sleeves": dict(
 title="Tattoo Sleeves in {city}, IL | {biz}",
 desc="Half and full tattoo sleeves by {artist} in {city}, IL. Planned as one composition and "
      "built across several sittings.",
 lede="Planned as one composition, then built in stages.",
 body="""
<p>There are two ways to end up with a sleeve. You can collect tattoos one at a time and hope they
eventually meet, or you can plan the whole arm first and then fill it in over a series of
sittings. The second way looks dramatically better and it is not more expensive, because you are
not paying to fix the gaps afterwards.</p>
<p>Planning first means deciding where the piece breathes. The empty skin in a good sleeve is
doing as much work as the imagery, and it is the first thing sacrificed when an arm gets filled
piecemeal.</p>
<p>You will be told up front how many sittings the plan takes and what happens in each one.</p>""",
 aside=("Half sleeves and full sleeves", "Existing work assessed and worked around",
        "Black and grey, color, or both", "Planned as one composition before the first session",
        "Booked as a series with a schedule you know in advance")),
}



STYLE_FAQ = {
"black-and-grey-chicano-realism": [
 ("How long does a black and grey sleeve take?",
  "You will be given a session count before anything is booked. A full sleeve is planned as one "
  "composition and then built in stages, so you always know what is coming next."),
 ("Is black and grey cheaper than color?",
  "Not by the hour. The rate is the same. Color often runs more sittings for the same area "
  "because the blends have to be packed properly, so a color version of the same design "
  "usually costs more overall."),
 ("Do you freehand the lettering?",
  "Script and Old English are drawn onto the skin rather than applied from a stencil, which is "
  "why the sizing conversation happens first. A wobble in freehand lettering is permanent."),
 ("Will grey wash fade faster than solid black?",
  "Grey is black pigment applied lighter, so lighter areas read softer as the piece settles. "
  "That is why the design leaves real negative space rather than filling every inch."),
],
"cover-up-tattoos": [
 ("Can any tattoo be covered?",
  "No. How dark and how solid the old ink is, how large you will let the new piece go, and "
  "where it sits all decide it. Send a photo and you will get a straight answer."),
 ("Will the old tattoo still show?",
  "The old tattoo does not disappear, it becomes shadow inside the new design. Done properly "
  "the eye stops finding it, which is why the new piece has to be bigger and darker."),
 ("Do I need laser fading first?",
  "Sometimes. A lightened base gives back the mid-tones a cover-up design needs for depth. "
  "If it is needed you will be told before booking, and we refer that work out."),
 ("Does a cover-up cost more than a fresh tattoo?",
  "Usually, because the same area needs more ink packed into it and often more sittings. The "
  "hourly rate is the same."),
],
"portrait-tattoos": [
 ("What kind of photo do you need?",
  "Sharp, well lit, straight on or three quarter, eyes in focus, nothing covering the face. "
  "A portrait can only hold the detail the photograph holds."),
 ("Can you work from an old or damaged photo?",
  "Sometimes, and it is the most common request for memorial work. Bring the best copy you "
  "have and you will hear honestly whether there is enough in it to work from."),
 ("How big does a portrait need to be?",
  "Bigger than most people first want. A face has to carry its features at the size it is "
  "tattooed, and shrinking it is what makes portraits go wrong."),
 ("Black and grey or color for a portrait?",
  "Most portraits are stronger in black and grey. Color adds a variable that has to be right "
  "on skin tone as well as likeness."),
],
"religious-tattoos": [
 ("Do I have to be religious to get one?",
  "No. Plenty of this imagery is family tradition rather than active practice, and nobody here "
  "is going to interview you about it."),
 ("What goes wrong with religious pieces?",
  "Usually scale. A Christ portrait in soft grey wash and tight script beside it need "
  "completely different handling, and cramming both into a small space ruins one of them."),
 ("Can you do Guadalupe or a specific saint?",
  "Yes. Bring the version you have in mind, because the iconography varies and the details "
  "matter to the people who will recognize it."),
],
"memorial-tattoos": [
 ("What should a memorial piece include?",
  "Most combine a portrait, a date, and imagery that meant something to the person. Getting "
  "those three to read as one composition is most of the work."),
 ("Should I wait before getting one?",
  "There is no rush from this side. Come in, talk it through, and let the drawing take the "
  "time it takes. This is the one piece nobody wants to redo."),
 ("Can you work from a handwritten note or signature?",
  "Yes, and a clear flat scan or photo of the original works better than a phone picture taken "
  "at an angle."),
],
"aztec-and-chicano-culture-tattoos": [
 ("Is the Aztec sun stone a calendar?",
  "It is commonly called the Aztec calendar, but the Sun Stone is a monumental carving rather "
  "than a working calendar. The imagery is what people want and it is worth getting right."),
 ("Why does the geometry matter so much?",
  "Because the stonework has real proportion in it. Rings out of true or guessed feather "
  "spacing read as wrong to anyone who knows the reference, which around here is a lot of "
  "people."),
 ("Color or black and grey for Aztec work?",
  "Both work. Headdresses and warrior pieces often carry color well, while stonework and "
  "medallions usually read stronger in black and grey."),
],
"color-realism-tattoos": [
 ("Does color hold up over time?",
  "Black pigment is carbon and holds its tone. Color pigments shift more, and some hold far "
  "better than others, which is why the palette gets decided before the first line."),
 ("Can I mix color with black and grey?",
  "Yes, and it is often the strongest version of the idea. A black and grey composition with "
  "one element carrying all the color."),
 ("Does color take longer?",
  "Usually, because the blends have to be packed properly or they go patchy. Expect more "
  "sittings than the same design in black and grey."),
],
"tattoo-sleeves": [
 ("How many sessions is a sleeve?",
  "It depends on the design, and you will be given the number before booking rather than "
  "after. Sleeves are booked as a series with dates you know in advance."),
 ("Can you work around tattoos I already have?",
  "Often, yes. Send photos of everything on the arm so the plan is built around what is "
  "actually there."),
 ("Should I plan the whole sleeve first?",
  "Yes. Collecting tattoos one at a time and hoping they meet is what produces the gaps you "
  "then pay to fix. Planning first is not more expensive."),
],
}

def build_style(sp):
    c = STYLE_COPY[sp["slug"]]
    fmt = dict(city=CITY, artist=ARTIST, biz=BIZ, phone=PHONE, years=YEARS, state=STATE)
    photos = by_tags(sp["tags"])
    tagged = len(photos)
    # A couple of categories have only a few tagged frames. Back them with the densest
    # large-scale work rather than showing a thin grid, and say so in the heading.
    if tagged < 8:
        extra = [m for m in MAN if m not in photos and
                 ("sleeve" in m["styles"] or m["quality"] >= 4)][:12 - tagged]
        photos = photos + extra
    figs = "".join(figure(m["slug"], sp["slug"] + "/") for m in photos)
    aside = "".join(f"<li>{x}</li>" for x in c["aside"])
    others = "".join(
        f'<a class="card" href="../{o["slug"]}/"><h3>{o["h1"]}</h3>'
        f'<p>{len(by_tags(o["tags"]))} pieces in the gallery</p></a>'
        for o in STYLE_PAGES if o["slug"] != sp["slug"])[:100000]
    qa = STYLE_FAQ.get(sp["slug"], [])
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in qa)
    extra = []
    if qa:
        extra.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in qa]})
    ld = {"@context": "https://schema.org", "@type": "Service",
          "serviceType": html.unescape(re.sub("<[^>]+>", "", sp["h1"])),
          "name": html.unescape(re.sub("<[^>]+>", "", sp["h1"])) + f" in {CITY}, {STATE}",
          "provider": {"@id": BASE + "/#shop"},
          "areaServed": [{"@type": "City", "name": a} for a in AREAS[:8]],
          "url": f"{BASE}/{sp['slug']}/"}
    hero = sp.get("hero") or photos[0]["slug"]
    if tagged >= 8:
        gal_heading = f'{sp["h1"]} in the gallery'
        gal_note = f"{len(photos)} pieces, all tattooed by {ARTIST}."
    else:
        gal_heading = f'{sp["h1"]}, and the scale this work takes'
        gal_note = (f"{tagged} tagged {'piece' if tagged == 1 else 'pieces'} in this category, "
                    f"shown alongside {len(photos) - tagged} large-scale pieces that show the "
                    f"density the work calls for. All tattooed by {ARTIST}.")
    return head(c["title"].format(**fmt), c["desc"].format(**fmt), sp["slug"] + "/",
                extra_ld=[ld] + extra,
                crumbs=[(html.unescape(re.sub("<[^>]+>", "", sp["h1"])), sp["slug"] + "/")],
                og_img=hero) + f"""
<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">{sp["nav"]}</p><h1>{sp["h1"]}</h1>
 <p>{c["lede"].format(**fmt)}</p></div>
 <div class="grid g2">
  <div>{c["body"].format(**fmt)}
   <p><a class="btn btn-p" href="tel:{TEL}">Call {PHONE}</a></p></div>
  <div><h3>What this covers</h3><ul class="areas" style="line-height:2.1">{aside}</ul>
   <div class="note" style="margin-top:20px">Serving {CITY}, Oak Lawn, Worth, Alsip, Palos
   Heights, Bridgeview, Burbank and Evergreen Park.</div></div>
 </div>
 <h2 style="margin-top:60px">{gal_heading}</h2>
 <p class="areas" style="margin-bottom:24px">{gal_note}</p>
 <div class="gal-grid">{figs}</div>
 <h2 style="margin-top:64px">Questions</h2>
 <div style="margin-top:22px">{faq_html}</div>
 <h2 style="margin-top:64px">Other work</h2>
 <div class="grid g4" style="margin-top:22px">{others}</div>
</div></section>
{visit(sp["slug"] + "/")}
{lightbox()}
""" + foot(sp["slug"] + "/")


# ==================================================================== ABOUT
def build_about():
    ld = {"@context": "https://schema.org", "@type": "Person",
          "@id": BASE + "/about/#nestor", "name": ARTIST, "alternateName": HANDLE,
          "jobTitle": "Owner and Tattoo Artist", "worksFor": {"@id": BASE + "/#shop"},
          "url": BASE + "/about/", "sameAs": [IG, FB, SNAP],
          "knowsAbout": ["Chicano tattooing", "Black and grey realism", "Cover-up tattooing",
                         "Portrait tattooing"],
          "address": {"@type": "PostalAddress", "addressLocality": CITY,
                      "addressRegion": STATE, "addressCountry": "US"}}
    return head(f"About {ARTIST} | Tattoo Artist in {CITY}, IL",
                f"{ARTIST}, owner and main tattoo artist at {BIZ} in {CITY}, IL. {YEARS} years "
                "tattooing black and grey Chicano realism, portraits and cover-ups.",
                "about/", extra_ld=[ld], crumbs=[("About", "about/")],
                og_img="tattoo-catrina-woman-with-roses") + f"""
<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">The artist</p><h1>{ARTIST}</h1>
 <p>Owner and main tattoo artist, {BIZ}.</p></div>
 <div class="grid g2">
  <div>
   <p>Nestor has been tattooing for {YEARS} years, working as <strong>{HANDLE}</strong>. He
   opened {BIZ} on 111th Street in {CITY} and still does most of the work in the shop
   himself.</p>
   <p>He does not limit himself to one style. Black and grey Chicano realism is what he is asked
   for most, the portraits and masks and script the style is built on, but the same week will
   take in color realism, Aztec and cultural work, memorials, anime and cover-ups.</p>
   <p>The shop runs on a straightforward principle: quality takes time and experience, and
   neither of those is cheap. If you are shopping on price he will tell you plainly that he is
   not your artist. If you want something drawn specifically for you, and built to still read in
   twenty years, that is the work.</p>
   <p>A lot of what comes through the door is faith-led. Christ portraits, scripture, memorial
   pieces for people who have been lost. That is deliberate, and the shop&rsquo;s name is not an
   accident.</p>
   <p style="font-size:1.15rem;color:var(--gold);font-weight:800">{TAGLINE}</p>
  </div>
  <div class="hero-img">{pic('tattoo-catrina-woman-with-roses', 1000,
                             'about/', sizes='(max-width:940px) 92vw, 46vw')}</div>
 </div>
 <div class="grid g4" style="margin-top:56px">
  <div class="card"><h3>{YEARS} years</h3><p>Tattooing professionally.</p></div>
  <div class="card"><h3>{GRATING} stars</h3><p>From {GCOUNT}
   <a href="{GBP}" rel="noopener">Google reviews</a>.</p></div>
  <div class="card"><h3>{RATE}/hour</h3><p>Shop rate. Smaller pieces quoted flat.</p></div>
  <div class="card"><h3>{len(MAN)} pieces</h3><p><a href="../gallery/">In the gallery</a>.</p></div>
 </div>
 <div class="cta" style="margin-top:36px">
  <a class="btn btn-p" href="../book/">Book a consultation</a>
  <a class="btn btn-s" href="../gallery/">See the work</a></div>
</div></section>
{reviews_block()}
{visit("about/")}
""" + foot("about/")


# ===================================================================== BOOK
def build_book():
    steps = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in STEPS)
    return head(f"Book a Tattoo | {BIZ}, {CITY}, IL",
                f"Send {ARTIST} your tattoo idea. {BIZ}, {STREET}, {CITY} IL. Text or call "
                f"{PHONE}. A deposit holds the date.",
                "book/", crumbs=[("Book", "book/")]) + f"""
<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">Booking</p><h1>Book a tattoo</h1>
 <p>Serious inquiries only. A deposit is required to hold any appointment.</p></div>
 <div class="grid g2">
  <div>
   <h3>Get in touch</h3>
   <p class="areas" style="line-height:2.3;font-size:1.04rem">
    <a href="tel:{TEL}">Call or text {PHONE}</a><br>
    <a href="{IG}" rel="noopener me">Instagram {IG_HANDLE}</a><br>
    <a href="{FB}" rel="noopener me">Facebook</a><br>
    <a href="mailto:{EMAIL}">{EMAIL}</a></p>
   <h3 style="margin-top:34px">What to send</h3>
   <ul class="areas" style="line-height:2.1">
    <li>A reference image or two</li>
    <li>Where on your body it goes</li>
    <li>Rough size in inches</li>
    <li>Black and grey, or color</li>
    <li>For a cover-up, a clear daylight photo of the existing tattoo</li>
   </ul>
   <div class="note" style="margin-top:22px">Bring a valid government-issued photo ID to your
   appointment. You must be 18 or older to be tattooed.</div>
   <div class="cta"><a class="btn btn-p" href="tel:{TEL}">Call {PHONE}</a></div>
  </div>
  <div>
   <h3>{BIZ}</h3>
   <address class="addr">{STREET}<br>{CITY}, {STATE} {ZIP}</address>
   <p style="margin-top:14px"><a href="{GBP}" rel="noopener">Get directions &rarr;</a></p>
   <h3 style="margin-top:32px">Hours</h3>{hours_table()}
   <p class="areas" style="margin-top:22px"><strong style="color:var(--tx)">Serving</strong><br>
   {", ".join(AREAS)}.</p>
  </div>
 </div>
 <h2 style="margin-top:64px">What happens next</h2>
 <ol class="steps" style="margin-top:24px">{steps}</ol>
</div></section>
""" + foot("book/")


def build_404():
    return head(f"Page not found | {BIZ}", "That page does not exist.", "") + f"""
<section><div class="narrow" style="text-align:center;padding:60px 0">
 <p class="eyebrow">404</p><h1>That page does not exist</h1>
 <p class="lede" style="margin:0 auto">The link may be old, or the address may have a typo in
 it. The gallery and the booking page are both one click away.</p>
 <div class="cta" style="justify-content:center">
  <a class="btn btn-p" href="/gallery/">See the gallery</a>
  <a class="btn btn-s" href="/">Home</a></div>
</div></section>
""" + foot()


# ================================================================== PRICING
PRICE_FAQ = [
 ("How much is a small tattoo?",
  "Small work is quoted as a flat price rather than by the hour, because a two inch piece takes "
  "more setup than needle time. Send the idea and the placement and you will get a number."),
 ("Is the deposit on top of the price?",
  "No. The deposit comes off the total. It is not a booking fee and it is not extra. It pays for "
  "the drawing time that happens before you sit down, which is work whether you show up or not."),
 ("Why will you not quote from a description alone?",
  "Because size, placement and how much detail sits in a given square inch change the number "
  "more than the subject does. A rose on a forearm and the same rose on a rib cage are not the "
  "same tattoo, and a photo of the spot settles it in seconds."),
 ("Do you price color differently from black and grey?",
  "Color usually takes longer for the same area because the blends have to be packed properly, "
  "so a color piece often runs more sittings than the black and grey version of the same "
  "design. The hourly rate does not change."),
 ("What if my piece needs more than one session?",
  "You are told the session count before anything is booked. Each sitting is billed at the "
  "hourly rate, and the deposit comes off the last one."),
]


def build_pricing():
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in PRICE_FAQ)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in PRICE_FAQ]}
    return head(f"Tattoo Prices in {CITY}, IL | {BIZ}",
                f"What a tattoo costs at {BIZ} in {CITY}, IL. Shop rate {RATE} an hour, small work "
                "quoted flat, deposit comes off the total.",
                "pricing/", extra_ld=[faq_ld], crumbs=[("Pricing", "pricing/")]) + f"""
<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">Pricing</p><h1>What a tattoo costs here</h1>
 <p>Nobody local publishes their rates. Here they are, so you can decide before you spend an
 afternoon messaging shops.</p></div>
 <div class="grid g2">
  <div>
   <h2>The short version</h2>
   <p>The shop rate is <strong>{RATE} an hour</strong> for large and ongoing work. Small pieces
   are quoted as a flat price instead, because a two inch tattoo takes far more setup than it
   takes needle time. A deposit holds your date and comes off the total.</p>
   <p>That rate is not a premium and it is not a bargain. It is what an experienced artist
   doing custom work in this area charges, and you should treat anyone quoting you a fraction
   of it as telling you something about the tattoo you are going to get.</p>
   <h2>What actually moves the number</h2>
   <ul class="areas" style="line-height:2.1">
    <li><strong>Size.</strong> The obvious one, and the one people underestimate.</li>
    <li><strong>Placement.</strong> Ribs, hands, feet and the inside of an arm are slower work
    than a flat outer forearm.</li>
    <li><strong>Detail density.</strong> A portrait and a piece of ornamental blackwork can be
    the same size and take twice as long.</li>
    <li><strong>Color versus black and grey.</strong> Color has to be packed properly, so it
    usually runs more sittings for the same area.</li>
    <li><strong>Whether it is a <a href="../cover-up-tattoos/">cover-up</a>.</strong> Covering
    old ink needs more ink into the same space, so it takes longer than a fresh piece of the
    same size.</li>
   </ul>
   <h2>How to get a real quote</h2>
   <p>Text the shop with four things and you will get a number back rather than a range: a
   reference image, the placement, a rough size in inches, and whether you want black and grey
   or color. For a cover-up, add a clear daylight photo of what is already there.</p>
   <div class="cta"><a class="btn btn-p" href="{SMS}">Text your idea</a>
   <a class="btn btn-s" href="tel:{TEL}">Call {PHONE}</a></div>
  </div>
  <div>
   <div class="card"><h3>Shop rate</h3>
    <p style="font-size:2rem;color:var(--gold);font-weight:800;margin:.2em 0">{RATE}/hour</p>
    <p>For large and ongoing work. Small pieces quoted flat.</p></div>
   <div class="card" style="margin-top:16px"><h3>Deposit</h3>
    <p>Required to hold any date. Comes off the total, never added to it.</p></div>
   <div class="card" style="margin-top:16px"><h3>Multi-session work</h3>
    <p>You get the session count before booking, not after. Each sitting is billed at the
    hourly rate.</p></div>
   <div class="note" style="margin-top:20px"><strong>Why there is no price list.</strong>
   A menu of per-piece prices invites people to shop a tattoo like a haircut. Every piece here
   is drawn for one person, so the honest version is a rate and a real quote.</div>
  </div>
 </div>
 <h2 style="margin-top:64px">Questions about price</h2>
 <div style="margin-top:24px">{faq}</div>
</div></section>
{visit("pricing/")}
""" + foot("pricing/")


# ================================================================== OAK LAWN
def build_oaklawn():
    photos = [m for m in MAN if m["quality"] >= 4][:12]
    figs = "".join(figure(m["slug"], "tattoo-artist-oak-lawn/") for m in photos)
    ld = {"@context": "https://schema.org", "@type": "Service",
          "serviceType": "Tattooing", "provider": {"@id": BASE + "/#shop"},
          "areaServed": {"@type": "City", "name": "Oak Lawn",
                         "containedInPlace": {"@type": "State", "name": "Illinois"}},
          "url": f"{BASE}/tattoo-artist-oak-lawn/"}
    return head("Tattoo Artist Near Oak Lawn, IL | Anointed Ink",
                f"{ARTIST} at {BIZ}, on 111th Street minutes from Oak Lawn. Black and grey "
                "Chicano realism, portraits and cover-ups.",
                "tattoo-artist-oak-lawn/", extra_ld=[ld],
                crumbs=[("Oak Lawn", "tattoo-artist-oak-lawn/")]) + f"""
<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">Oak Lawn</p>
 <h1>A tattoo artist a few minutes from Oak Lawn</h1>
 <p>{BIZ} sits on 111th Street in {CITY}, right on the Oak Lawn line.</p></div>
 <div class="grid g2">
  <div>
   <p>If you live in Oak Lawn, the shop is closer than most of the places you will find by
   searching the village itself. We are at {STREET}, west along 111th Street, which for most
   of Oak Lawn is a shorter run than heading north into the city and a lot easier to park
   for.</p>
   <p>A good number of the pieces in <a href="../gallery/">the gallery</a> belong to people
   from Oak Lawn, Worth and Burbank. This is a neighborhood shop, not a destination studio,
   and most of the work here comes from within about fifteen minutes of the door.</p>
   <h2>What people come here for</h2>
   <p>Mostly <a href="../black-and-grey-chicano-realism/">black and grey Chicano realism</a>,
   which is {ARTIST}&rsquo;s signature and which almost nobody else in the southwest suburbs
   is set up for. After that it is <a href="../portrait-tattoos/">portraits</a>,
   <a href="../memorial-tattoos/">memorial pieces</a>,
   <a href="../religious-tattoos/">religious work</a> and
   <a href="../cover-up-tattoos/">cover-ups</a>.</p>
   <h2>Getting here from Oak Lawn</h2>
   <p>Take 111th Street west. On the Chicago street grid we are at 5920 west, which puts us
   between Central Avenue and Ridgeland Avenue, with parking at the door.</p>
   <div class="cta"><a class="btn btn-p" href="{SMS}">Text your idea</a>
   <a class="btn btn-s" href="{GBP}" rel="noopener">Get directions</a></div>
  </div>
  <div>
   <div class="card"><h3>{BIZ}</h3>
    <address class="addr" style="font-size:.98rem">{STREET}<br>{CITY}, {STATE} {ZIP}<br>
    <a href="tel:{TEL}">{PHONE}</a></address>
    <p style="margin-top:12px">Mon to Sat, 12pm to 7pm. Closed Sunday.</p></div>
   <div class="card" style="margin-top:16px"><h3>Also serving</h3>
    <p>{", ".join(a for a in AREAS if a != "Oak Lawn")}.</p></div>
   <div class="note" style="margin-top:16px">{GRATING} stars from {GCOUNT}
   <a href="{GBP}" rel="noopener">Google reviews</a>, as of {RATING_AS_OF}.</div>
  </div>
 </div>
 <h2 style="margin-top:60px">Recent work</h2>
 <div class="gal-grid" style="margin-top:22px">{figs}</div>
</div></section>
{visit("tattoo-artist-oak-lawn/")}
{lightbox()}
""" + foot("tattoo-artist-oak-lawn/")


# =================================================================== SPANISH
def build_spanish():
    photos = by_tags(["chicano", "aztec-cultural", "religious"], 12)
    figs = "".join(figure(m["slug"], "es/tatuajes-estilo-chicano/") for m in photos)
    alt = ('<link rel="alternate" hreflang="en" href="' + BASE +
           '/black-and-grey-chicano-realism/">'
           '<link rel="alternate" hreflang="es" href="' + BASE + '/es/tatuajes-estilo-chicano/">'
           '<link rel="alternate" hreflang="x-default" href="' + BASE +
           '/black-and-grey-chicano-realism/">')
    p = "es/tatuajes-estilo-chicano/"
    return head("Tatuajes Estilo Chicano en Chicago Ridge, IL | Anointed Ink",
                f"Tatuajes estilo chicano en negro y gris por {ARTIST} en {CITY}, IL. Retratos, "
                f"piezas religiosas y cubrimientos. {PHONE}.",
                p, extra_head=alt,
                og_img="tattoo-catrina-woman-with-roses") + f"""
<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">En espa&ntilde;ol</p>
 <h1>Tatuajes estilo chicano en {CITY}</h1>
 <p>Negro y gris, retratos, piezas religiosas y trabajo azteca, hechos a mano por
 {ARTIST} en {BIZ}.</p></div>
 <div class="grid g2">
  <div>
   <p>El estilo chicano en negro y gris no es un tatuaje a color al que le quitaron el color.
   Todo se construye con contraste: qu&eacute; tan oscuros son los negros, qu&eacute; tan
   pareja queda la aguada gris, y cu&aacute;nta piel se deja libre. Si ese equilibrio sale
   mal, la pieza se convierte en una mancha gris en cinco a&ntilde;os.</p>
   <p>Es un estilo con su propio lenguaje: letra fina y old english, las m&aacute;scaras de
   r&iacute;e ahora, llora despu&eacute;s, catrinas, la Virgen de Guadalupe, rosarios, relojes
   y rosas, y retratos de familia. La letra es lo m&aacute;s dif&iacute;cil, porque se dibuja
   a mano alzada sobre la piel y un temblor queda para siempre.</p>
   <p>{ARTIST} lleva {YEARS} a&ntilde;os tatuando y este es el trabajo que m&aacute;s le
   piden. Tambi&eacute;n hace <a href="../../cover-up-tattoos/">cubrimientos</a>,
   <a href="../../portrait-tattoos/">retratos</a>,
   <a href="../../memorial-tattoos/">piezas en memoria</a> y
   <a href="../../aztec-and-chicano-culture-tattoos/">trabajo azteca</a>.</p>
   <h2>C&oacute;mo agendar</h2>
   <p>Manda un mensaje de texto al {PHONE} con tu idea, d&oacute;nde la quieres, el
   tama&ntilde;o aproximado en pulgadas, y si la quieres en negro y gris o a color. Si es un
   cubrimiento, manda tambi&eacute;n una foto clara con luz de d&iacute;a del tatuaje que ya
   tienes.</p>
   <p>Se requiere un dep&oacute;sito para apartar la fecha, y ese dep&oacute;sito se descuenta
   del total. Debes tener 18 a&ntilde;os o m&aacute;s y traer identificaci&oacute;n oficial con foto
   y fecha de nacimiento. En Illinois no existe el permiso de los padres para tatuar a un
   menor.</p>
   <div class="cta"><a class="btn btn-p" href="{SMS}">Mandar mi idea</a>
   <a class="btn btn-s" href="tel:{TEL}">Llamar {PHONE}</a></div>
  </div>
  <div>
   <div class="card"><h3>{BIZ}</h3>
    <address class="addr" style="font-size:.98rem">{STREET}<br>{CITY}, {STATE} {ZIP}<br>
    <a href="tel:{TEL}">{PHONE}</a></address>
    <p style="margin-top:12px">Lunes a s&aacute;bado, 12pm a 7pm. Domingo cerrado.</p>
    <p>{RATE} por hora.</p></div>
   <div class="note" style="margin-top:16px">{GRATING} estrellas de {GCOUNT}
   <a href="{GBP}" rel="noopener">rese&ntilde;as en Google</a>.</div>
   <p style="margin-top:18px"><a href="../../black-and-grey-chicano-realism/">Read this page in
   English &rarr;</a></p>
  </div>
 </div>
 <h2 style="margin-top:60px">El trabajo</h2>
 <div class="gal-grid" style="margin-top:22px">{figs}</div>
</div></section>
{lightbox()}
""" + foot(p)


# ===================================================================== BLOG
BLOG_POSTS = []
if os.path.exists("blog/posts.json"):
    BLOG_POSTS = json.load(open("blog/posts.json"))


def expand_images(body, path):
    """Turn [[IMG:slug|caption]] placeholders into responsive figures."""
    def sub(m):
        slug, _, cap = m.group(1).partition("|")
        slug = slug.strip()
        if slug not in BYSLUG:
            return ""
        cap = html.escape(cap.strip() or BYSLUG[slug]["caption"])
        return (f'<figure>{pic(slug, 1000, path, sizes="(max-width:820px) 92vw, 760px")}'
                f"<figcaption>{cap}</figcaption></figure>")
    return re.sub(r"\[\[IMG:([^\]]+)\]\]", sub, body)


def slugify_heading(h):
    return re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub("<[^>]+>", "", h)).lower()).strip("-")


def build_post(p, prev_p, next_p):
    path = f"blog/{p['slug']}/"
    body = expand_images(p["html"], path)
    # anchor the h2s so the table of contents works
    def anchor_h2(m):
        txt = m.group(1)
        return f'<h2 id="{slugify_heading(txt)}">{txt}</h2>'
    body = re.sub(r"<h2>(.*?)</h2>", anchor_h2, body, flags=re.S)

    heads = p.get("headings") or re.findall(r'<h2 id="[^"]*">(.*?)</h2>', body, re.S)
    toc = ""
    if len(heads) >= 3:
        items = "".join(
            f'<li><a href="#{slugify_heading(h)}">{re.sub("<[^>]+>", "", h)}</a></li>'
            for h in heads)
        toc = f'<nav class="toc"><h2>On this page</h2><ol>{items}</ol></nav>'

    hero = p.get("hero")
    ld = [{
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": p["title"], "description": p["metaDescription"],
        "datePublished": BUILT, "dateModified": BUILT,
        "inLanguage": "en-US",
        "author": {"@type": "Person", "@id": BASE + "/about/#nestor", "name": ARTIST},
        "publisher": {"@id": BASE + "/#shop"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{BASE}/{path}"},
        "wordCount": len(re.sub("<[^>]+>", " ", body).split()),
    }]
    if hero:
        ld[0]["image"] = f"{BASE}/img/{hero}-1000.webp"
    if p.get("faq"):
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"],
             "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in p["faq"]]})

    nav = []
    if prev_p:
        nav.append(f'<a class="card" href="../{prev_p["slug"]}/"><h3>&larr; '
                   f'{prev_p["title"]}</h3><p>{prev_p["excerpt"]}</p></a>')
    if next_p:
        nav.append(f'<a class="card" href="../{next_p["slug"]}/"><h3>{next_p["title"]} '
                   f'&rarr;</h3><p>{next_p["excerpt"]}</p></a>')
    navhtml = f'<div class="grid g2" style="margin-top:48px">{"".join(nav)}</div>' if nav else ""

    faqhtml = ""
    if p.get("faq"):
        faqhtml = ("<h2>Quick answers</h2>" + "".join(
            f"<details><summary>{f['q']}</summary><p>{f['a']}</p></details>"
            for f in p["faq"]))

    # no brand suffix on post titles: the headline is already long and the SERP truncates
    return head(p["title"], p["metaDescription"], path,
                extra_ld=ld, crumbs=[("Blog", "blog/"), (p["title"], path)],
                og_img=hero or "og",
                preload=hero) + f"""
<section><div class="narrow">
 <p class="eyebrow"><a href="../" style="color:var(--gold)">Blog</a></p>
 <h1>{p["title"]}</h1>
 <p class="byline">By {ARTIST}, owner and tattoo artist at
 <a href="../../about/">{BIZ}</a> &middot; {p.get("readMinutes", 6)} min read</p>
 {toc}
 <article class="prose">{body}{faqhtml}</article>
 <div class="note" style="margin-top:40px"><strong>Want to talk about a piece?</strong>
 Text {PHONE} with your idea, the placement and a rough size, and you will get a straight
 answer back. <a href="../../pricing/">Rates and deposits</a> are published.</div>
 <div class="cta"><a class="btn btn-p" href="{SMS}">Text your idea</a>
 <a class="btn btn-s" href="../../gallery/">See the gallery</a></div>
 {navhtml}
</div></section>
""" + foot(path)


def build_blog_index():
    cards = ""
    for p in BLOG_POSTS:
        thumb = ""
        if p.get("hero"):
            thumb = f'<div class="thumb">{pic(p["hero"], 400, "blog/")}</div>'
        cards += (f'<a class="post" href="{p["slug"]}/">{thumb}'
                  f'<div class="body"><span class="kicker">{p.get("kicker","Guide")}</span>'
                  f'<h3>{p["title"]}</h3><p>{p["excerpt"]}</p>'
                  f'<span class="meta">{p.get("readMinutes",6)} min read</span></div></a>')
    ld = {"@context": "https://schema.org", "@type": "Blog",
          "name": f"The {BIZ} blog", "url": f"{BASE}/blog/",
          "publisher": {"@id": BASE + "/#shop"},
          "blogPost": [{"@type": "BlogPosting", "headline": p["title"],
                        "url": f"{BASE}/blog/{p['slug']}/", "datePublished": BUILT,
                        "author": {"@id": BASE + "/about/#nestor"}} for p in BLOG_POSTS]}
    return head(f"Tattoo Guides and Advice | {BIZ}",
                f"Straight answers on cover-ups, Chicano black and grey, portraits, pricing and "
                f"booking, written by {ARTIST} in {CITY}, IL.",
                "blog/", extra_ld=[ld], crumbs=[("Blog", "blog/")]) + f"""
<section><div class="wrap">
 <div class="sec-head"><p class="eyebrow">Blog</p><h1>Straight answers about tattoos</h1>
 <p>Written by {ARTIST}. No filler, no top ten lists. The questions people actually ask before
 they book, answered the way they get answered in the shop.</p></div>
 <div class="posts">{cards}</div>
</div></section>
{visit("blog/")}
""" + foot("blog/")


# ==================================================================== WRITE
def emit():
    write("index.html", build_home())
    write("gallery/index.html", build_gallery())
    for sp in STYLE_PAGES:
        write(f"{sp['slug']}/index.html", build_style(sp))
    write("pricing/index.html", build_pricing())
    write("tattoo-artist-oak-lawn/index.html", build_oaklawn())
    write("es/tatuajes-estilo-chicano/index.html", build_spanish())
    write("about/index.html", build_about())
    write("book/index.html", build_book())
    if BLOG_POSTS:
        write("blog/index.html", build_blog_index())
        for i, p in enumerate(BLOG_POSTS):
            write(f"blog/{p['slug']}/index.html",
                  build_post(p, BLOG_POSTS[i - 1] if i else None,
                             BLOG_POSTS[i + 1] if i + 1 < len(BLOG_POSTS) else None))
    write("404.html", build_404())

    for path, content in PAGES.items():
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        open(path, "w").write(content)

    urls = [""] + [p[:-len("index.html")] for p in PAGES
                   if p.endswith("index.html") and p != "index.html"]
    open("robots.txt", "w").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n" if INDEXABLE
        else "User-agent: *\nDisallow: /\n")
    def imgs_for(u):
        if u != "gallery/":
            return ""
        return "".join(
            f"<image:image><image:loc>{BASE}/img/{m['slug']}-1000.webp</image:loc>"
            f"<image:caption>{html.escape(m['alt'])}</image:caption></image:image>"
            for m in MAN)
    sm = "".join(
        f"<url><loc>{BASE}/{u}</loc><lastmod>{BUILT}</lastmod>"
        f"<priority>{'1.0' if u == '' else '0.8'}</priority>{imgs_for(u)}</url>" for u in urls)
    open("sitemap.xml", "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
        f'{sm}</urlset>')
    open(".nojekyll", "w").write("")
    return urls


if __name__ == "__main__":
    urls = emit()
    print(f"pages: {len(PAGES)}   photos: {len(MAN)}   noindex: {not INDEXABLE}")
    for p in sorted(PAGES): print("  ", p)
