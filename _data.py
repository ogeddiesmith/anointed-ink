# -*- coding: utf-8 -*-
"""
Verified facts for anointedink.

Every value here was checked against a named public source on 2026-09-24 and the
source is recorded in ../CLIENT-BRIEF.md. Do not add a value without one.
"""

# ---- launch switches -------------------------------------------------------
INDEXABLE = False                                    # noindex until Nestor approves
BASE = "https://ogeddiesmith.github.io/anointed-ink" # Pages origin; swap for the real domain
BUILT = "2026-09-24"

# ---- NAP, matches the Google Business Profile exactly ----------------------
BIZ    = "Anointed Ink"
ARTIST = "Nestor Juarez"
HANDLE = "Tat2Nestuhh"
STREET = "5920 W 111th St"
CITY   = "Chicago Ridge"
STATE  = "IL"
STATE_FULL = "Illinois"
ZIP    = "60415"
PHONE  = "(708) 770-2754"
TEL    = "+17087702754"
EMAIL  = "anointed.ink29@gmail.com"
LAT, LNG = 41.6907469, -87.7673829
PLUSCODE = "M6RM+72 Chicago Ridge, Illinois"
RATE   = "$150"          # his Instagram bio. CONFIRM
YEARS  = "25+"           # his Popl card and Instagram bio. His own claim.
GRATING, GCOUNT = "5.0", "115"    # Google Business Profile

GBP = "https://www.google.com/maps/place/Anointed+Ink/@41.6907469,-87.7673829,672m"
IG  = "https://www.instagram.com/tat2nestuhh/"
IG_HANDLE = "@tat2nestuhh"
FB  = "https://www.facebook.com/ghtto.mex/"
FBPAGE = "https://www.facebook.com/profile.php?id=61590253627999"
SNAP = "https://www.snapchat.com/add/tat2nestuh0610"

HOURS = [(d, "12:00", "19:00") for d in
         ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")]
HOURS_HUMAN = "Monday to Saturday, 12pm to 7pm. Closed Sunday."

AREAS = ["Chicago Ridge", "Oak Lawn", "Worth", "Alsip", "Palos Heights", "Bridgeview",
         "Burbank", "Evergreen Park", "Hometown", "Palos Hills", "Hickory Hills",
         "Chicago's Southwest Side"]

TAGLINE = "Don't be average. Be set apart."

# ---- verified Google reviews ----------------------------------------------
REVIEWS = [
    # Verbatim from the Google Business Profile, including original spelling and punctuation.
    # 16 CFR 255.0(b): editing a review so it no longer fairly reflects its substance is
    # deceptive, so these are NOT cleaned up. Ellipsis only where the review continues.
    ("Owner and Main Tattoo Artist Nestor never disappoints. I Have had 2 tattoos done by Nestor "
     "one was a complete cover up and the 2nd was a partial cover up and add on&hellip;",
     "Timothy C."),
    ("I always have a good experience getting tattooed by Nestor- his artwork is top notch and "
     "always keeps me coming back!", "Marie E."),
    ("We got 2 tattoos that look like stickers!! Awesome work I loved the work so much I booked "
     "another appointment! Book it dont wait!", "Sean M."),
]
# Deliberately NOT republished: a review opening "Best tattoo shop in town". Lifting it onto our
# own site converts it into our own superiority claim (16 CFR 255.0(b) Example 1), which 815 ILCS
# 510/2(a)(7) reaches and which four named local rivals have a private right of action over.

RATING_AS_OF = "September 24, 2026"   # date-stamp the rating so it is true-as-of, not a promise

# ---- contact routes, ordered by how Nestor actually works -------------------
SMS_BODY = ("Hi Nestor, I saw your site.%0A%0AIdea:%0APlacement:%0ARough size in inches:"
            "%0ABlack and grey or color:%0ACover-up (yes/no):%0ABest days for me:")
SMS = f"sms:{TEL}?&body={SMS_BODY}"
IG_DM = "https://ig.me/m/tat2nestuhh"

# ---- Illinois rules we are allowed to state, with citations -----------------
LAW_AGE = ("18 and over, no exceptions. Illinois law does not allow a parent to consent to a "
           "minor being tattooed (720 ILCS 5/12C-35).")
LAW_ID = ("Bring a government-issued photo ID showing your date of birth. Illinois rules require "
          "the shop to verify age from it every visit, including for people we already know "
          "(77 Ill. Adm. Code 797.400(k)).")
LAW_MINORS_PRESENT = ("Anyone under 18 has to be with a parent or legal guardian just to be on "
                      "the premises while tattooing is happening (720 ILCS 5/12C-35(b)).")

# ---- style pages -----------------------------------------------------------
# slug, nav label, h1, style tags pulled from the photo manifest
STYLE_PAGES = [
    dict(slug="black-and-grey-chicano-realism", nav="Black &amp; Grey",
         h1="Black &amp; grey Chicano realism",
         tags=["chicano", "black-and-grey-realism"], hero="tattoo-catrina-woman-with-roses"),
    dict(slug="cover-up-tattoos", nav="Cover-Ups", h1="Cover-up tattoos",
         tags=["cover-up"], hero="tattoo-crowned-skull-cover-up"),
    dict(slug="portrait-tattoos", nav="Portraits", h1="Portrait tattoos",
         tags=["portrait"], hero="tattoo-woman-and-lioness-split-portrait"),
    dict(slug="religious-tattoos", nav="Religious", h1="Religious tattoos",
         tags=["religious"], hero=None),
    dict(slug="memorial-tattoos", nav="Memorials", h1="Memorial tattoos",
         tags=["memorial"], hero=None),
    dict(slug="aztec-and-chicano-culture-tattoos", nav="Aztec &amp; Cultural",
         h1="Aztec and cultural tattoos",
         tags=["aztec-cultural"], hero="tattoo-aztec-warrior-bear"),
    dict(slug="color-realism-tattoos", nav="Color", h1="Color realism tattoos",
         tags=["color-realism"], hero=None),
    dict(slug="tattoo-sleeves", nav="Sleeves", h1="Tattoo sleeves",
         tags=["sleeve"], hero=None),
]

# human labels for the gallery filter chips
STYLE_LABELS = {
    "black-and-grey-realism": "Black &amp; grey realism",
    "chicano": "Chicano",
    "portrait": "Portraits",
    "religious": "Religious",
    "memorial": "Memorials",
    "aztec-cultural": "Aztec &amp; cultural",
    "color-realism": "Color realism",
    "animal": "Animals",
    "floral": "Floral",
    "sleeve": "Sleeves",
    "lettering-script": "Script &amp; lettering",
    "ornamental": "Ornamental",
    "cover-up": "Cover-ups",
    "anime-character": "Anime &amp; characters",
    "fine-line": "Fine line",
}

# ---- main nav --------------------------------------------------------------
NAV = [("", "Home"), ("gallery/", "Gallery"),
       ("black-and-grey-chicano-realism/", "Black &amp; Grey"),
       ("cover-up-tattoos/", "Cover-Ups"), ("pricing/", "Pricing"),
       ("blog/", "Blog"), ("about/", "About"), ("book/", "Send your idea")]
