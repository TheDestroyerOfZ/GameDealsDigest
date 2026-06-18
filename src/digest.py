"""
digest.py — the CONTENT ENGINE. Turns the list of deals into things you can publish:
  - an HTML page (your website / index.html)
  - a Markdown post (paste into Blogger / WordPress)
  - ready-to-paste social captions (Pinterest / X / Reddit)

This is the part that replaces the "daily grind" from those make-money videos: the
program writes the daily content for you, so maintenance stays near zero.
"""

import config
from src.affiliate import deal_link

_PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{site} — {date}</title>
<meta name="description" content="{tagline} Updated {date}.">
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; font-family:system-ui,Segoe UI,Roboto,sans-serif; background:#0f1115; color:#e7e9ee; }}
  header {{ padding:28px 16px; text-align:center; background:linear-gradient(135deg,#1b2030,#0f1115); }}
  header h1 {{ margin:0; font-size:1.8rem; }}
  header p {{ margin:6px 0 0; color:#9aa3b2; }}
  .grid {{ max-width:1100px; margin:24px auto; padding:0 16px; display:grid;
           grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:16px; }}
  .card {{ background:#171a21; border:1px solid #242833; border-radius:12px; overflow:hidden;
           display:flex; flex-direction:column; transition:transform .1s; }}
  .card:hover {{ transform:translateY(-3px); }}
  .card img {{ width:100%; height:120px; object-fit:cover; background:#0b0d11; }}
  .info {{ padding:12px 14px; display:flex; flex-direction:column; gap:8px; flex:1; }}
  .info h3 {{ margin:0; font-size:1rem; line-height:1.3; }}
  .price {{ margin:0; }}
  .sale {{ color:#7ee787; font-weight:700; font-size:1.1rem; }}
  .normal {{ color:#717b8c; text-decoration:line-through; margin-left:6px; font-size:.85rem; }}
  .save {{ background:#2ea043; color:#fff; border-radius:6px; padding:1px 6px; font-size:.8rem; margin-left:6px; }}
  .store {{ margin:0; color:#9aa3b2; font-size:.82rem; }}
  .buy {{ margin-top:auto; text-align:center; background:#2563eb; color:#fff; text-decoration:none;
          padding:8px; border-radius:8px; font-weight:600; }}
  .buy:hover {{ background:#1d4ed8; }}
  footer {{ text-align:center; color:#717b8c; font-size:.8rem; padding:24px 16px; }}
</style></head>
<body>
<header><h1>🎮 {site}</h1><p>{tagline} · Updated {date}</p></header>
<main class="grid">
{cards}
</main>
<footer>Prices from CheapShark and may change. Some links may be affiliate links.
Updated {date}.</footer>
</body></html>"""

_CARD = """  <div class="card">
    {thumb}
    <div class="info">
      <h3>{title}</h3>
      <p class="price"><span class="sale">${sale:.2f}</span>
        <span class="normal">${normal:.2f}</span><span class="save">-{save}%</span></p>
      <p class="store">{store}</p>
      <a class="buy" href="{link}" target="_blank" rel="nofollow noopener">See deal</a>
    </div>
  </div>"""


def build_html(deals, date_str):
    """The publishable web page."""
    cards = []
    for d in deals:
        thumb = (f'<img src="{d["thumb"]}" alt="{d["title"]}" loading="lazy">'
                 if d.get("thumb") else "")
        cards.append(_CARD.format(thumb=thumb, title=d["title"], sale=d["sale_price"],
                                  normal=d["normal_price"], save=d["savings_pct"],
                                  store=d["store"], link=deal_link(d)))
    return _PAGE.format(site=config.SITE_NAME, tagline=config.SITE_TAGLINE,
                        date=date_str, cards="\n".join(cards))


def build_markdown(deals, date_str):
    """A blog post you can paste into Blogger / WordPress."""
    lines = [f"# {config.SITE_NAME} — {date_str}", "", config.SITE_TAGLINE, ""]
    for d in deals:
        lines.append(f"- **[{d['title']}]({deal_link(d)})** — "
                     f"**${d['sale_price']:.2f}** (was ${d['normal_price']:.2f}, "
                     f"-{d['savings_pct']}%) · {d['store']}")
    lines += ["", "_Prices from CheapShark and may change. Some links may be affiliate links._"]
    return "\n".join(lines)


def build_social(deals, date_str):
    """Ready-to-paste captions for Pinterest / X / Reddit."""
    top = deals[0] if deals else None
    out = [f"=== SOCIAL CAPTIONS — {date_str} ===", ""]
    if top:
        out += [f"[Pinterest / X]",
                f"🎮 Today's top PC game deal: {top['title']} is {top['savings_pct']}% off "
                f"— just ${top['sale_price']:.2f} on {top['store']}! More daily deals 👇",
                ""]
    out.append("[Reddit / forum post]")
    out.append(f"Best PC game deals today ({date_str}):")
    for d in deals[:8]:
        out.append(f"• {d['title']} — ${d['sale_price']:.2f} (-{d['savings_pct']}%) @ {d['store']}")
    return "\n".join(out)
