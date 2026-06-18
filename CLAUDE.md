# CLAUDE.md — Game Deals Digest

This file is auto-loaded by Claude Code when this folder is opened. It carries the
context and decisions from the original build session so a fresh window is instantly
up to speed. (The companion stock-prediction project lives in `Desktop\MyNewProject`
and is intentionally on the back burner — do not touch it.)

## What this project is
An **automated daily PC game-deals site**. `run_daily.py` pulls current deals from the
free **CheapShark API** (no key, no scraping), filters to quality real games, and
generates publishable output: a web page, a blog-post markdown file, and social
captions. The point is **low-maintenance automation** — set it up once, schedule it,
it updates itself.

## Who the user is (important for how to help)
- A capable **hobbyist coder** (Python), based in **New Zealand**. Likes **gaming**.
- **Values honesty above hype** — this is the #1 thing. Never fake numbers, never
  oversell income potential. They explicitly rejected "get-rich-quick" / 20%-a-month
  /emotional-manipulation-marketing approaches. Be the honest voice.
- Wants **low-maintenance, runs-itself** projects and **free/local tools** (no paid
  services unless truly necessary). Beginner-friendly, well-commented code.
- The real goal is a **portfolio/career asset** (LinkedIn) more than direct income —
  the projects are proof of skill, which is their actual money path.

## Honest framing to maintain (don't drift from this)
- The **automation runs itself** (the low-maintenance win), but **getting traffic is
  the manual part code can't do**, and the **deals niche is crowded** (r/GameDeals,
  IsThereAnyDeal). Realistic income: **$0–50/month**, likely pocket money at best.
- It's worth doing anyway because it costs **~$0** to run and is a strong **shipped,
  live portfolio piece** — frame it as learning + portfolio, with ad/affiliate income
  as a small bonus, NOT as an income play.

## How it works (architecture)
- `config.py` — all settings (stores, price range, min discount, quality gate,
  affiliate tags, branding). Edit this, not the code.
- `run_daily.py` — the one command: fetch → build → save to `output/`.
- `src/stores.py` — store ID → name map (cached to `output/.stores_cache.json`).
- `src/deals.py` — fetch (paginated) + filter + de-dupe. **Quality gate**: only real
  games with ≥100 Steam reviews & ≥70% positive (this kills DLC/asset-pack spam — a
  problem we hit and fixed; the first run was flooded with RPG Maker DLC).
- `src/affiliate.py` — builds the buy link (CheapShark redirect by default; real
  affiliate deep links go in `config.AFFILIATE` once approved).
- `src/digest.py` — the content engine: builds the HTML page, markdown post, and
  social captions.
- `output/` — generated files (`index.html` is always the latest). This is what gets
  published.

## How to run / test
```powershell
# one-time
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# each run
.\.venv\Scripts\python.exe run_daily.py
```
Note: PowerShell 5.1's old TLS defaults make raw API calls 400; Python `requests`
is fine, so test through the Python script, not Invoke-RestMethod.

## Status & next steps
**Status:** built, working, tested locally. Generates a clean deals page. NOT yet
deployed or monetised.

**Planned next steps (in order):**
1. **Go live for free** — GitHub Pages (static hosting) + **GitHub Actions cron** to
   run `run_daily.py` daily and auto-publish, so it self-updates without the user's PC
   on. ~$0 (optional ~$12/yr custom domain). This was the next task when we paused.
2. **Polish `README.md`** for public/recruiter eyes.
3. **Draft a LinkedIn post** about the deals site — angle: "built & shipped a fully
   automated, self-deploying site," lead with the engineering/automation, not "buy
   deals." LinkedIn is for showcasing skill to employers, not deals-site traffic.
4. Optional features: free-games tracker (Epic/Steam), bigger thumbnails, RSS, a
   "biggest discounts" section.
5. Monetisation (later): apply to Fanatical/Green Man Gaming/Humble affiliate
   programs, add tags to `config.AFFILIATE`; optionally AdSense on the live page.

## Conventions
- Keep code **beginner-friendly and well-commented**, settings in `config.py`.
- Keep all captions/disclaimers **honest** (prices may change; some links may be
  affiliate links; no income hype).
- Output text is consumed by Streamlit-free plain files; avoid emojis in console
  `print()`s if it ever causes Windows cp1252 errors (use ASCII markers).
