# Design system for anointedink. Plain string, not an f-string: braces are literal.
CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
 --bg:#08080a; --bg2:#0e0e12; --surface:#141419; --surface2:#1b1b22;
 --line:#26262f; --line2:#33333f;
 --tx:#f0eeea; --muted:#9d988f; --muted2:#8a847b;
 --gold:#c9a24a; --gold2:#e5c584; --gold-dim:rgba(201,162,74,.14);
 --max:1200px; --gut:24px; --r:14px; --rs:10px;
 --f: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
body{margin:0;background:var(--bg);color:var(--tx);font:400 17px/1.72 var(--f);
 -webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;height:auto;display:block}
a{color:var(--gold2);text-decoration-thickness:1px;text-underline-offset:3px}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:4px}
h1,h2,h3,h4{line-height:1.12;margin:0 0 .5em;letter-spacing:-.025em;font-weight:800}
h1{font-size:clamp(2.2rem,6.2vw,4.2rem)}
h2{font-size:clamp(1.7rem,3.8vw,2.7rem)}
h3{font-size:1.2rem;font-weight:700;letter-spacing:-.012em}
p{margin:0 0 1.15em}
hr{border:0;border-top:1px solid var(--line);margin:44px 0}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--gut)}
.narrow{max-width:760px;margin:0 auto;padding:0 var(--gut)}
.eyebrow{font:700 .74rem/1 var(--f);letter-spacing:.24em;text-transform:uppercase;
 color:var(--gold);margin:0 0 1.15em}
.skip{position:absolute;left:-9999px}
.skip:focus{left:12px;top:12px;z-index:200;background:var(--gold);color:#12100b;
 padding:11px 18px;border-radius:8px;font-weight:700}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
 clip:rect(0 0 0 0);white-space:nowrap;border:0}

/* ---------- header ---------- */
header{position:sticky;top:0;z-index:90;background:rgba(8,8,10,.9);
 backdrop-filter:saturate(1.5) blur(12px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;gap:8px;min-height:68px}
.brand{font-weight:800;letter-spacing:.15em;text-transform:uppercase;font-size:.95rem;
 color:var(--tx);text-decoration:none;margin-right:auto;white-space:nowrap}
.brand span{color:var(--gold)}
.navlinks{display:flex;align-items:center;gap:22px}
.navlinks a{color:var(--muted);text-decoration:none;font-size:.93rem;font-weight:600;white-space:nowrap}
.navlinks a:hover,.navlinks a[aria-current=page]{color:var(--tx)}
.callbtn{background:var(--gold);color:#14100a;padding:10px 18px;border-radius:999px;
 font-weight:800;text-decoration:none;font-size:.9rem;white-space:nowrap;margin-left:14px}
.callbtn:hover{background:var(--gold2)}
.burger{display:none;background:none;border:1px solid var(--line);border-radius:9px;
 color:var(--tx);width:42px;height:38px;cursor:pointer;font-size:1.1rem;line-height:1}

/* ---------- hero ---------- */
.hero{position:relative;border-bottom:1px solid var(--line);
 background:radial-gradient(120% 90% at 78% 12%,rgba(201,162,74,.11),transparent 62%)}
.hero-grid{display:grid;grid-template-columns:1.06fr .94fr;gap:56px;align-items:center;
 padding-top:86px;padding-bottom:90px}  /* top/bottom only: .wrap owns the side gutter */
.tagline{font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--gold);
 font-size:clamp(.92rem,1.9vw,1.1rem);margin:0 0 1.25em}
.lede{font-size:1.15rem;color:var(--muted);max-width:54ch}
.cta{display:flex;gap:13px;flex-wrap:wrap;margin-top:32px}
.btn{display:inline-block;padding:15px 28px;border-radius:999px;font-weight:800;
 text-decoration:none;font-size:1rem;border:1px solid transparent;cursor:pointer}
.btn-p{background:var(--gold);color:#14100a}
.btn-p:hover{background:var(--gold2)}
.btn-s{border-color:var(--line2);color:var(--tx);background:var(--surface)}
.btn-s:hover{border-color:var(--gold);background:var(--surface2)}
.hero-img{border-radius:var(--r);overflow:hidden;border:1px solid var(--line);
 box-shadow:0 30px 70px rgba(0,0,0,.6)}
.hero-img img{width:100%;aspect-ratio:3/4;object-fit:cover;object-position:50% 36%}

/* ---------- trust ---------- */
.trust{border-bottom:1px solid var(--line);background:var(--bg2)}
.trust-in{display:flex;gap:14px 30px;flex-wrap:wrap;justify-content:space-between;
 padding:19px 0;font-size:.95rem;color:var(--muted)}
.trust b{color:var(--tx)}
.stars{color:var(--gold);letter-spacing:.06em}

section{padding:84px 0}
section+section{border-top:1px solid var(--line)}
.sec-head{max-width:66ch;margin-bottom:42px}
.sec-head p{color:var(--muted);margin:0}
.alt{background:var(--bg2)}

/* ---------- grids + cards ---------- */
.grid{display:grid;gap:18px}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);
 padding:28px;display:flex;flex-direction:column}
.card h3{margin-bottom:.45em}
.card p{color:var(--muted);font-size:.97rem;margin:0}
.card .more{margin-top:auto;padding-top:16px;font-weight:700;font-size:.95rem}
a.card{text-decoration:none;color:inherit;transition:border-color .18s,transform .18s}
a.card:hover{border-color:var(--gold);transform:translateY(-2px)}

/* ---------- gallery ---------- */
.filters{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:26px}
.chip{background:var(--surface);border:1px solid var(--line);color:var(--muted);
 border-radius:999px;padding:9px 17px;font:600 .88rem/1 var(--f);cursor:pointer}
.chip:hover{color:var(--tx);border-color:var(--line2)}
.chip[aria-pressed=true]{background:var(--gold);border-color:var(--gold);color:#14100a}
.masonry{column-count:4;column-gap:14px}
.masonry figure{margin:0 0 14px;break-inside:avoid;border-radius:var(--rs);overflow:hidden;
 border:1px solid var(--line);background:var(--surface);position:relative;cursor:zoom-in}
.masonry img{width:100%;transition:transform .5s ease,opacity .3s}
.masonry figure:hover img{transform:scale(1.04)}
.masonry figcaption{position:absolute;left:0;right:0;bottom:0;padding:26px 14px 11px;
 font-size:.83rem;color:#fff;opacity:0;transition:opacity .22s;
 background:linear-gradient(transparent,rgba(0,0,0,.86))}
.masonry figure:hover figcaption,.masonry figure:focus-within figcaption{opacity:1}
.masonry figure[hidden]{display:none}
.gal-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:13px}
.gal-grid figure{margin:0;border-radius:var(--rs);overflow:hidden;border:1px solid var(--line);
 background:var(--surface);aspect-ratio:1;cursor:zoom-in}
.gal-grid img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.gal-grid figure:hover img{transform:scale(1.045)}
.count{color:var(--muted2);font-size:.9rem;margin-bottom:22px}

/* ---------- lightbox ---------- */
.lb{position:fixed;inset:0;z-index:150;background:rgba(5,5,7,.96);display:none;
 align-items:center;justify-content:center;padding:28px}
.lb[open],.lb.on{display:flex}
.lb figure{margin:0;max-width:min(1100px,94vw);max-height:90vh;display:flex;
 flex-direction:column;align-items:center;gap:14px}
.lb img{max-height:78vh;width:auto;border-radius:var(--rs);border:1px solid var(--line2)}
.lb figcaption{color:var(--muted);font-size:.94rem;text-align:center;max-width:62ch}
.lb button{position:absolute;background:rgba(20,20,25,.9);border:1px solid var(--line2);
 color:var(--tx);width:48px;height:48px;border-radius:50%;cursor:pointer;font-size:1.3rem;
 line-height:1;display:grid;place-items:center}
.lb button:hover{border-color:var(--gold)}
.lb .x{top:20px;right:20px}
.lb .prev{left:20px;top:50%;transform:translateY(-50%)}
.lb .next{right:20px;top:50%;transform:translateY(-50%)}

/* ---------- reviews / steps / faq ---------- */
.rev{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:28px}
.rev blockquote{margin:0 0 16px;font-size:1.03rem}
.rev cite{font-style:normal;color:var(--muted);font-size:.89rem;font-weight:600}
ol.steps{list-style:none;counter-reset:s;padding:0;margin:0;display:grid;gap:15px}
ol.steps li{counter-increment:s;background:var(--surface);border:1px solid var(--line);
 border-radius:var(--r);padding:25px 28px 25px 72px;position:relative}
ol.steps li::before{content:counter(s);position:absolute;left:25px;top:23px;width:31px;height:31px;
 border-radius:50%;background:var(--gold);color:#14100a;font-weight:800;display:grid;
 place-items:center;font-size:.9rem}
ol.steps h3{margin-bottom:.3em}
ol.steps p{color:var(--muted);margin:0;font-size:.97rem}
details{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);
 padding:21px 25px;margin-bottom:12px}
details[open]{border-color:var(--line2)}
summary{cursor:pointer;font-weight:700;font-size:1.03rem;list-style:none;display:flex;
 justify-content:space-between;gap:18px;align-items:flex-start}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--gold);font-weight:800;font-size:1.3rem;line-height:1}
details[open] summary::after{content:"\\2013"}
details p{margin:15px 0 0;color:var(--muted);font-size:.98rem}
details p:last-child{margin-bottom:0}

/* ---------- visit ---------- */
.visit{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.addr{font-style:normal;font-size:1.06rem;line-height:1.85}
table.hrs{border-collapse:collapse;width:100%;font-size:.97rem}
table.hrs th,table.hrs td{text-align:left;padding:10px 0;border-bottom:1px solid var(--line);
 font-weight:500;color:var(--muted)}
table.hrs th{color:var(--tx);font-weight:600}
table.hrs tr:last-child th,table.hrs tr:last-child td{border-bottom:0}
.areas{color:var(--muted);font-size:.96rem}
.note{background:var(--surface2);border:1px solid var(--line);border-left:3px solid var(--gold);
 border-radius:8px;padding:17px 21px;color:var(--muted);font-size:.95rem}
.note strong{color:var(--tx)}

/* ---------- blog ---------- */
.posts{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.post{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);
 overflow:hidden;text-decoration:none;color:inherit;display:flex;flex-direction:column;
 transition:border-color .18s,transform .18s}
.post:hover{border-color:var(--gold);transform:translateY(-2px)}
.post .thumb{aspect-ratio:16/10;overflow:hidden;background:var(--surface2)}
.post .thumb img{width:100%;height:100%;object-fit:cover}
.post .body{padding:22px 24px 26px;display:flex;flex-direction:column;flex:1}
.post h3{font-size:1.08rem;margin-bottom:.5em}
.post p{color:var(--muted);font-size:.93rem;margin:0}
.post .kicker{font:700 .7rem/1 var(--f);letter-spacing:.18em;text-transform:uppercase;
 color:var(--gold);margin-bottom:12px}
.post .meta{margin-top:auto;padding-top:16px;color:var(--muted2);font-size:.83rem}

article.prose{font-size:1.07rem;line-height:1.78}
article.prose h2{margin-top:2em;font-size:clamp(1.45rem,3vw,2rem)}
article.prose h3{margin-top:1.7em;font-size:1.18rem}
article.prose ul,article.prose ol{margin:0 0 1.25em;padding-left:1.3em;color:var(--tx)}
article.prose li{margin-bottom:.5em}
article.prose blockquote{margin:1.7em 0;padding:20px 26px;background:var(--surface);
 border-left:3px solid var(--gold);border-radius:0 8px 8px 0;color:var(--tx);font-size:1.05rem}
article.prose blockquote p:last-child{margin-bottom:0}
article.prose figure{margin:2em 0}
article.prose figure img{border-radius:var(--rs);border:1px solid var(--line);width:100%}
article.prose figcaption{color:var(--muted2);font-size:.87rem;margin-top:10px;text-align:center}
.tbl{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:1.6em 0}
article.prose table{width:100%;border-collapse:collapse;margin:0;font-size:.96rem}
article.prose th,article.prose td{border:1px solid var(--line);padding:11px 14px;text-align:left}
article.prose th{background:var(--surface);color:var(--tx);font-weight:700}
article.prose td{color:var(--muted)}
.byline{color:var(--muted2);font-size:.9rem;margin-bottom:2.2em}
.toc{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);
 padding:22px 26px;margin-bottom:2.4em}
.toc h2{font-size:.76rem!important;letter-spacing:.18em;text-transform:uppercase;
 color:var(--gold);margin:0 0 14px!important}
.toc ol{margin:0;padding-left:1.15em}
.toc li{margin-bottom:.42em;font-size:.96rem}
.toc a{color:var(--muted);text-decoration:none}
.toc a:hover{color:var(--gold2)}

/* ---------- footer + sticky bar ---------- */
footer{border-top:1px solid var(--line);background:var(--bg2);padding:58px 0 44px;
 color:var(--muted);font-size:.93rem}
.foot{display:grid;grid-template-columns:1.8fr 1fr 1fr 1fr;gap:34px}
footer a{color:var(--muted);text-decoration:none}
footer a:hover{color:var(--gold2)}
footer h3{color:var(--tx);font-size:.76rem;letter-spacing:.17em;text-transform:uppercase;
 margin-bottom:1.1em}
.foot ul{list-style:none;padding:0;margin:0;line-height:2.05}
.legal{border-top:1px solid var(--line);margin-top:40px;padding-top:24px;font-size:.85rem;
 color:var(--muted2)}
.stickybar{display:none;position:fixed;left:0;right:0;bottom:0;z-index:95;
 background:rgba(8,8,10,.97);backdrop-filter:blur(10px);border-top:1px solid var(--line);
 padding:10px 14px;gap:10px}
.stickybar a{flex:1;text-align:center;padding:13px 10px;border-radius:999px;font-weight:800;
 text-decoration:none;font-size:.95rem}

/* ---------- responsive ---------- */
@media(max-width:1040px){
 .masonry{column-count:3}
 .foot{grid-template-columns:1fr 1fr}
}
@media(max-width:940px){
 .hero-grid{grid-template-columns:1fr;gap:38px;padding-top:54px;padding-bottom:60px}
 .g3,.g4{grid-template-columns:repeat(2,1fr)}
 .gal-grid{grid-template-columns:repeat(3,1fr)}
 .posts{grid-template-columns:repeat(2,1fr)}
 .visit{grid-template-columns:1fr}
 .navlinks{display:none;position:absolute;top:100%;left:0;right:0;flex-direction:column;
  align-items:stretch;gap:0;background:var(--bg2);border-bottom:1px solid var(--line);padding:8px 0}
 .navlinks.open{display:flex}
 .navlinks a{padding:14px var(--gut);font-size:1rem;border-top:1px solid var(--line)}
 .burger{display:block;order:3}
 .callbtn{margin-left:auto;order:2}
 header{position:relative}
}
@media(max-width:640px){
 section{padding:56px 0}
 .g2,.g3,.g4{grid-template-columns:1fr}
 .masonry{column-count:2;column-gap:10px}
 .masonry figure{margin-bottom:10px}
 .gal-grid{grid-template-columns:repeat(2,1fr)}
 .posts{grid-template-columns:1fr}
 .foot{grid-template-columns:1fr}
 .stickybar{display:flex}
 .callbtn{display:none}  /* the sticky bar carries Call; the pill pushed the menu button off-screen */
 body{padding-bottom:68px}
 .lb{padding:12px}
 .lb .prev{left:8px}.lb .next{right:8px}
 .lb button{width:42px;height:42px}
 ol.steps li{padding:22px 22px 22px 64px}
}
"""
