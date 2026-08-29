# -*- coding: utf-8 -*-
"""
Generuje:
  - realizacie/<slug>.html  pre kazdy projekt v content/realizacie/*.json
  - vlozi cerstvu mriezku projektov do realizacie.html (medzi filter-bar a cta-band)
  - vlozi vyber projektov do index.html (sekcia "Nasa praca")
Spustenie: python3 tools/build_realizacie.py
"""
import os, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "content", "realizacie")

with open(os.path.join(ROOT, "tools", "jsonld_snippet.html"), encoding="utf-8") as _f:
    JSONLD = _f.read().strip()

CAT_LABELS = {
    "novostavby": "Novostavby",
    "rekonstrukcie": "Rekonštrukcie",
    "opornemury": "Oporné múry",
    "inestavby": "Iné stavby",
}

ICON_ARROW_UR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg>'
ICON_ARROW_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'

ALT_BY_CAT = {
    "novostavby": "Hrubá stavba rodinného domu — {place}",
    "rekonstrukcie": "Rekonštrukcia domu — {place}",
    "opornemury": "Oporný múr — {place}",
    "inestavby": "Stavebné práce NOVYS s.r.o. — {place}",
}

def seo_alt(p):
    primary = p["cats"][0] if p.get("cats") else "inestavby"
    town = p["place"].split(",")[0].strip()
    return ALT_BY_CAT.get(primary, "Realizácia NOVYS s.r.o. — {place}").format(place=town)

def load_projects():
    items = []
    for fp in glob.glob(os.path.join(CONTENT_DIR, "*.json")):
        with open(fp, encoding="utf-8") as f:
            items.append(json.load(f))
    items.sort(key=lambda p: p["order"])
    return items

def cats_badges(cats):
    return "".join('<span class="project-tag">{}</span>'.format(CAT_LABELS[c]) for c in cats)

def cats_data(cats):
    return " ".join(cats)

def nav_html(root, active_key):
    def link(href, label, key):
        cls = ' class="active"' if key == active_key else ""
        return '<a href="{root}{href}"{cls}>{label}</a>'.format(root=root, href=href, cls=cls, label=label)
    return """
<header class="site-header">
  <div class="container">
    <a href="{root}index.html" class="brand">
      <img src="{root}assets/img/site/logo_light.png" alt="NOVYS s.r.o.">
    </a>
    <nav class="main-nav">
      <div class="mobile-menu-head"><a href="{root}index.html" class="mobile-menu-logo"><img src="{root}assets/img/site/logo_light.png" alt="NOVYS s.r.o."></a><button class="nav-close" aria-label="Zavrieť menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg></button></div>
      <ul>
        <li>{home}</li>
        <li class="has-drop">
          <a href="#">Firma</a>
          <div class="dropdown"><ul>
            <li><a href="{root}o-nas.html">O nás</a></li>
            <li><a href="{root}nase-sluzby.html">Naše služby</a></li>
          </ul></div>
        </li>
        <li class="has-drop">
          {real}
          <div class="dropdown"><ul>
            <li><a href="{root}realizacie.html?kategoria=novostavby">Novostavby</a></li>
            <li><a href="{root}realizacie.html?kategoria=rekonstrukcie">Rekonštrukcie</a></li>
            <li><a href="{root}realizacie.html?kategoria=opornemury">Oporné múry</a></li>
            <li><a href="{root}realizacie.html?kategoria=inestavby">Iné stavby</a></li>
          </ul></div>
        </li>
        <li>{kontakt}</li>
      </ul>
      <div class="mobile-menu-contact">
        <a href="tel:+421903537023" class="mobile-menu-call"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span>+421 903 537 023</span></a>
        <a href="{root}kontakt.html" class="btn btn-primary btn-block">Nezáväzná cenová ponuka</a>
        <div class="mobile-menu-meta"><span>Žilina a okolie</span><a href="mailto:kontakt@novys.sk">kontakt@novys.sk</a></div>
      </div>
    </nav>
    <div class="header-cta">
      <a href="tel:+421903537023" class="header-phone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span>+421 903 537 023</span></a>
      <a href="{root}kontakt.html" class="btn btn-primary btn-sm">Cenová ponuka</a>
      <button class="nav-toggle" aria-label="Menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ><path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/></svg></button>
    </div>
  </div>
</header>
""".format(root=root, home=link("index.html", "Úvod", "domov"), real=link("realizacie.html", "Realizácie", "realizacie"), kontakt=link("kontakt.html", "Kontakt", "kontakt"))

def footer_html(root):
    return """
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{root}assets/img/site/logo_light.png" alt="NOVYS s.r.o.">
        <p>Rodinná stavebná firma so sídlom v Žiline. Viac ako 15 rokov budujeme domy a riešenia, ktoré vydržia celé generácie.</p>
      </div>
      <div class="footer-col">
        <h5>Firma</h5>
        <ul>
          <li><a href="{root}o-nas.html">O nás</a></li>
          <li><a href="{root}nase-sluzby.html">Naše služby</a></li>
          <li><a href="{root}realizacie.html">Realizácie</a></li>
          <li><a href="{root}kontakt.html">Kontakt</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Realizácie</h5>
        <ul>
          <li><a href="{root}realizacie.html?kategoria=novostavby">Novostavby</a></li>
          <li><a href="{root}realizacie.html?kategoria=rekonstrukcie">Rekonštrukcie</a></li>
          <li><a href="{root}realizacie.html?kategoria=opornemury">Oporné múry</a></li>
          <li><a href="{root}realizacie.html?kategoria=inestavby">Iné stavby</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Kontakt</h5>
        <ul class="footer-contact">
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg><span>NOVYS s.r.o.<br>Dunajská 1467/21, 010 01 Žilina</span></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg><a href="tel:+421903537023">+421 903 537 023</a></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg><a href="mailto:kontakt@novys.sk">kontakt@novys.sk</a></li>
                  </ul>
        <div class="footer-map">
          <iframe src="https://www.google.com/maps?q=NOVYS+s.r.o.,+Dunajsk%C3%A1+1467/21,+010+01+%C5%BDilina&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa — NOVYS s.r.o."></iframe>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year></span> NOVYS s.r.o. Všetky práva vyhradené.</span>
      <span>IČO: 47960531 &nbsp;·&nbsp; DIČ: 2024163680 &nbsp;·&nbsp; IČ DPH: SK2024163680</span>
    </div>
  </div>
</footer>
""".format(root=root)

HEAD_TPL = """<!DOCTYPE html>
<html lang="sk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{root}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{root}assets/img/site/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{root}assets/img/site/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="{root}assets/img/site/apple-touch-icon.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{ogimg}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#15181d">
<link rel="stylesheet" href="{root}assets/css/style.css?v=21">
{jsonld}
</head>
<body>
"""

FOOT_TPL = """
<script src="{root}assets/js/main.js?v=9"></script>
</body>
</html>
"""

def project_page(p, prev_p, next_p):
    root = "../"
    hero_url = root + p["hero"]

    alt_text = seo_alt(p)
    gallery_imgs = "".join(
        '<img src="{u}" loading="lazy" alt="{t}" data-lightbox="{u}">'.format(u=root + g["image"], t=alt_text)
        for g in p["gallery"] if g.get("image")
    )

    typelist = ", ".join(CAT_LABELS[c] for c in p["cats"])
    year_html = p["year"] if p["year"] else "—"

    body = """
{header}

<section class="project-hero" style="background-image:url('{hero}')">
  <div class="container">
    <div class="breadcrumb"><a href="{root}index.html">Úvod</a><span>/</span><a href="{root}realizacie.html">Realizácie</a><span>/</span><span>{title}</span></div>
    <h1>{title}</h1>
    <div class="project-tags">{tags}</div>
    <div class="project-meta">
      <div><span>Lokalita</span><b>{place}</b></div>
      <div><span>Rok realizácie</span><b>{year}</b></div>
      <div><span>Typ stavby</span><b>{typelist}</b></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="two-col reveal">
      <div>
        <div class="eyebrow">O realizácii</div>
        <h2>{title}</h2>
        <p>{desc}</p>
      </div>
      <div><img src="{hero}" alt="{alt_text}" style="border-radius:18px;box-shadow:var(--shadow-lg)" data-lightbox="{hero}"></div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    <div class="section-head reveal"><div class="eyebrow">Fotogaléria</div><h2>Priebeh realizácie</h2></div>
    <div class="gallery-strip reveal">{gallery}</div>
  </div>
</section>

<section class="container">
  <div class="related-nav reveal">
    <a href="{root}realizacie/{pslug}.html">← {ptitle}</a>
    <a href="{root}realizacie.html">Všetky realizácie</a>
    <a href="{root}realizacie/{nslug}.html">{ntitle} →</a>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    <div class="cta-band reveal">
      <div><h2>Páči sa vám táto realizácia?</h2><p>Ozvite sa nám — pripravíme cenovú ponuku šitú na mieru vášmu pozemku.</p></div>
      <div class="actions"><a href="{root}kontakt.html" class="btn btn-primary">{arrow}Nezáväzná cenová ponuka</a></div>
    </div>
  </div>
</section>

{footer}
""".format(
        header=nav_html(root, "realizacie"),
        hero=hero_url, root=root, title=p["title"], tags=cats_badges(p["cats"]),
        place=p["place"], year=year_html, typelist=typelist, desc=p["description"],
        gallery=gallery_imgs, alt_text=alt_text,
        pslug=prev_p["slug"], ptitle=prev_p["title"], nslug=next_p["slug"], ntitle=next_p["title"],
        arrow=ICON_ARROW_R,
        footer=footer_html(root),
    )

    desc_meta = "{} — {}. Realizácia stavebnej firmy NOVYS s.r.o. z okolia Žiliny.".format(p["title"], typelist)
    year_bit = " ({})".format(p["year"]) if p["year"] else ""
    html = HEAD_TPL.format(
        title="{} — {}{} — Realizácie NOVYS s.r.o.".format(p["title"], typelist, year_bit),
        desc=desc_meta, ogimg=hero_url, root=root, jsonld=JSONLD,
    ) + body + FOOT_TPL.format(root=root)
    return html


def project_card(p, root=""):
    img = root + p["hero"]
    return """
      <a class="project-card mix reveal" data-cats="{cats}" href="{root}realizacie/{slug}.html">
        <img src="{img}" alt="{alt_text}" loading="lazy">
        <span class="project-arrow">{arrow}</span>
        <div class="project-info">
          <div class="project-tags">{tags}</div>
          <h3>{title}</h3>
          <span>{place}</span>
        </div>
      </a>
    """.format(cats=cats_data(p["cats"]), root=root, slug=p["slug"], img=img, title=p["title"],
               arrow=ICON_ARROW_UR, tags=cats_badges(p["cats"]), place=p["place"], alt_text=seo_alt(p))


def main():
    projects = load_projects()
    n = len(projects)
    print("Loaded", n, "projects")

    os.makedirs(os.path.join(ROOT, "realizacie"), exist_ok=True)
    for i, p in enumerate(projects):
        prev_p = projects[(i - 1) % n]
        next_p = projects[(i + 1) % n]
        html = project_page(p, prev_p, next_p)
        with open(os.path.join(ROOT, "realizacie", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
    print("Wrote", n, "detail pages")

    # ---- update realizacie.html grid ----
    cards_html = "".join(project_card(p, root="") for p in projects)
    filter_bar = """<div class="filter-bar reveal" data-filter-bar>
      <button class="filter-btn is-active" data-filter="all">Všetky realizácie</button>
      <button class="filter-btn" data-filter="novostavby">Novostavby</button>
      <button class="filter-btn" data-filter="rekonstrukcie">Rekonštrukcie</button>
      <button class="filter-btn" data-filter="opornemury">Oporné múry</button>
      <button class="filter-btn" data-filter="inestavby">Iné stavby</button>
    </div>"""

    listing_path = os.path.join(ROOT, "realizacie.html")
    with open(listing_path, encoding="utf-8") as f:
        listing = f.read()

    import re
    listing = re.sub(
        r'<div class="filter-bar reveal" data-filter-bar>.*?</div>\s*<div class="projects-grid">.*?</div>\s*</div>\s*</section>',
        filter_bar + '\n    <div class="projects-grid">' + cards_html + '</div>\n  </div>\n</section>',
        listing, flags=re.S,
    )
    with open(listing_path, "w", encoding="utf-8") as f:
        f.write(listing)
    print("Updated realizacie.html grid (", n, "cards )")

    # ---- update index.html featured projects ----
    featured = projects[:6]
    featured_html = "".join("""
      <a class="project-card reveal" href="realizacie/{slug}.html">
        <img src="{hero}" alt="{alt_text}" loading="lazy">
        <span class="project-arrow">{arrow}</span>
        <div class="project-info">
          <div class="project-tags">{tags}</div>
          <h3>{title}</h3>
          <span>{place}</span>
        </div>
      </a>
    """.format(slug=p["slug"], hero=p["hero"], title=p["title"], tags=cats_badges(p["cats"]),
               place=p["place"], arrow=ICON_ARROW_UR, alt_text=seo_alt(p)) for p in featured)

    index_path = os.path.join(ROOT, "index.html")
    with open(index_path, encoding="utf-8") as f:
        index_html = f.read()
    new_index_html = re.sub(
        r'(<div class="projects-grid">).*?(</div>\s*<div style="text-align:center;margin-top:44px">)',
        r'\1' + featured_html + r'\2',
        index_html, flags=re.S,
    )
    if new_index_html == index_html:
        print("WARNING: index.html projects-grid pattern not matched, no changes made")
    else:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_index_html)
        print("Updated index.html featured projects (", len(featured), "cards )")


if __name__ == "__main__":
    main()
