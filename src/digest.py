"""
digest.py — the CONTENT ENGINE. Turns the deals into things you can publish:
  - an HTML page (your website) with themed sections, rich cards, and live search
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
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family:system-ui,Segoe UI,Roboto,sans-serif; background:#0f1115; color:#e7e9ee; }}
  header {{ padding:34px 16px 22px; text-align:center; background:linear-gradient(135deg,#1b2030,#0f1115); }}
  header h1 {{ margin:0; font-size:2rem; letter-spacing:.3px; }}
  header p {{ margin:6px 0 0; color:#9aa3b2; }}
  .stats {{ margin:16px auto 0; display:flex; gap:10px; justify-content:center; flex-wrap:wrap; }}
  .stat {{ background:#171a21; border:1px solid #242833; border-radius:999px; padding:6px 14px; font-size:.85rem; color:#c7ccd6; }}
  .stat b {{ color:#7ee787; }}
  .searchwrap {{ max-width:1100px; margin:20px auto 0; padding:0 16px; }}
  #search {{ width:100%; padding:12px 16px; border-radius:10px; border:1px solid #2a2f3a;
             background:#13161c; color:#e7e9ee; font-size:1rem; }}
  section {{ max-width:1100px; margin:30px auto; padding:0 16px; }}
  section h2 {{ font-size:1.25rem; margin:0 0 14px; border-left:4px solid #2563eb; padding-left:10px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:16px; }}
  .card {{ background:#171a21; border:1px solid #242833; border-radius:12px; overflow:hidden;
           display:flex; flex-direction:column; transition:transform .1s, border-color .1s; }}
  .card:hover {{ transform:translateY(-3px); border-color:#2563eb; }}
  .card img {{ width:100%; height:130px; object-fit:cover; background:#0b0d11; }}
  .info {{ padding:12px 14px; display:flex; flex-direction:column; gap:8px; flex:1; }}
  .info h3 {{ margin:0; font-size:1rem; line-height:1.3; }}
  .price {{ margin:0; }}
  .sale {{ color:#7ee787; font-weight:700; font-size:1.15rem; }}
  .normal {{ color:#717b8c; text-decoration:line-through; margin-left:6px; font-size:.85rem; }}
  .save {{ background:#2ea043; color:#fff; border-radius:6px; padding:1px 6px; font-size:.8rem; margin-left:6px; }}
  .badges {{ display:flex; gap:6px; flex-wrap:wrap; }}
  .badge {{ font-size:.72rem; padding:2px 7px; border-radius:6px; background:#0e1a2b; color:#9ecbff; border:1px solid #1d3a55; }}
  .badge.steam {{ background:#16261a; color:#8be39a; border:1px solid #234a2e; }}
  .badge.meta {{ background:#2a1f0e; color:#ffce8b; border:1px solid #43331a; }}
  .store {{ margin:0; color:#9aa3b2; font-size:.82rem; }}
  .buy {{ margin-top:auto; text-align:center; background:#2563eb; color:#fff; text-decoration:none;
          padding:9px; border-radius:8px; font-weight:600; }}
  .buy:hover {{ background:#1d4ed8; }}
  .noresults {{ text-align:center; color:#717b8c; padding:30px; display:none; }}
  footer {{ text-align:center; color:#717b8c; font-size:.8rem; padding:30px 16px; max-width:720px; margin:0 auto; line-height:1.5; }}
  footer a {{ color:#9ecbff; }}
</style></head>
<body>
<header>
  <h1>🎮 {site}</h1>
  <p>{tagline}</p>
  <div class="stats">
    <span class="stat"><b>{count}</b> deals today</span>
    <span class="stat">up to <b>-{max_save}%</b> off</span>
    <span class="stat">updated {date}</span>
  </div>
</header>
<div class="searchwrap"><input id="search" type="search" placeholder="🔍 Search games..."></div>
{sections}
<p class="noresults" id="noresults">No games match your search.</p>
<footer>
  <p>{site} surfaces the best current PC game discounts from across the major stores, refreshed daily.</p>
  <p>Prices are sourced from <a href="https://www.cheapshark.com" rel="noopener">CheapShark</a> and can
  change at any time — always confirm the final price on the store page before buying.</p>
  <p>Some links may be affiliate links: we may earn a small commission at no extra cost to you.</p>
  <p>Updated {date} · Educational/personal project · Not affiliated with any store.</p>
</footer>
<script>
  const q = document.getElementById('search'), nr = document.getElementById('noresults');
  q.addEventListener('input', () => {{
    const v = q.value.toLowerCase(); let shown = 0;
    document.querySelectorAll('.card').forEach(c => {{
      const hit = c.dataset.title.includes(v);
      c.style.display = hit ? '' : 'none'; if (hit) shown++;
    }});
    document.querySelectorAll('section').forEach(s => {{
      s.style.display = [...s.querySelectorAll('.card')].some(c => c.style.display !== 'none') ? '' : 'none';
    }});
    nr.style.display = shown ? 'none' : 'block';
  }});
</script>
</body></html>"""


def _card(d):
    thumb = (f'<img src="{d["thumb"]}" alt="{d["title"]}" loading="lazy">'
             if d.get("thumb") else "")
    badges = []
    if d.get("steam_pct"):
        rc = f' ({d["steam_reviews"]:,})' if d.get("steam_reviews") else ''
        badges.append(f'<span class="badge steam">👍 {d["steam_pct"]}%{rc}</span>')
    if d.get("metacritic"):
        badges.append(f'<span class="badge meta">Metacritic {d["metacritic"]}</span>')
    badges_html = "".join(badges)
    return f"""  <div class="card" data-title="{d['title'].lower()}">
    {thumb}
    <div class="info">
      <h3>{d['title']}</h3>
      <p class="price"><span class="sale">${d['sale_price']:.2f}</span>
        <span class="normal">${d['normal_price']:.2f}</span><span class="save">-{d['savings_pct']}%</span></p>
      <div class="badges">{badges_html}</div>
      <p class="store">{d['store']}</p>
      <a class="buy" href="{deal_link(d)}" target="_blank" rel="nofollow noopener">See deal →</a>
    </div>
  </div>"""


def build_html(sections, date_str, pool):
    """The publishable web page, built from themed sections."""
    blocks = []
    for s in sections:
        cards = "\n".join(_card(d) for d in s["deals"])
        blocks.append(f'<section><h2>{s["title"]}</h2>\n<div class="grid">\n{cards}\n</div></section>')
    max_save = max((d["savings_pct"] for d in pool), default=0)
    return _PAGE.format(site=config.SITE_NAME, tagline=config.SITE_TAGLINE, date=date_str,
                        count=len(pool), max_save=max_save, sections="\n".join(blocks))


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
