# 🎮 Game Deals Digest

An automated daily PC game-deals site. One scheduled command fetches the best current
deals from the free [CheapShark](https://apidocs.cheapshark.com/) API (no key, no
scraping), filters to quality games, enriches genres from Steam, and generates a
self-contained web page — with curated highlight sections and a searchable, sortable,
filterable "Browse All" view. Set it up once and it updates itself daily via GitHub
Actions, hosted free on GitHub Pages.

## Features
- Live deals across major stores (Steam, GOG, Fanatical, Humble, Green Man Gaming, …)
- Quality gate — only real games with genuine Steam reviews (filters out DLC/asset spam)
- Genre tags (via Steam) + Steam rating, review count, and Metacritic on each card
- Browse tool — search + genre / store / price / sort, all client-side
- Multi-currency display (USD source, converted via live rates) + a price disclaimer
- Self-updating every 8 hours in the cloud (GitHub Actions) — no server, $0 to run

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run
```powershell
.\.venv\Scripts\python.exe run_daily.py
```
This writes to `output/`:
- `index.html` — the website (latest deals)
- `deals-YYYY-MM-DD.html` — a dated archive copy
- `deals-YYYY-MM-DD.md` — a blog post (Blogger / WordPress)
- `social-YYYY-MM-DD.txt` — social captions

## Deploy (free)
See [DEPLOY.md](DEPLOY.md) — GitHub Pages plus a GitHub Actions cron rebuild the site
daily, with no server and no cost.

## Configure
Everything adjustable lives in [config.py](config.py): stores, price range, minimum
discount, quality thresholds, pool size, branding, and affiliate tags.

## Monetisation
Affiliate links from third-party stores (Fanatical, Green Man Gaming, Humble) — add your
tags to `AFFILIATE` in [config.py](config.py) once approved; optionally add display ads.
(Steam has no affiliate program, so the value is third-party stores, which are often
cheaper than Steam anyway.)

## Project layout
```
GameDealsDigest/
├── config.py          <- settings (edit this, not the code)
├── run_daily.py       <- the one command: fetch -> enrich -> build -> save
├── requirements.txt   <- dependencies (requests)
├── src/
│   ├── stores.py      <- store id -> name (cached)
│   ├── deals.py       <- fetch + filter + de-dupe (data engine)
│   ├── genres.py      <- genre enrichment via Steam (cached, fails softly)
│   ├── affiliate.py   <- builds the buy link
│   └── digest.py      <- builds the page / blog post / social captions
└── .github/workflows/ <- daily auto-build + deploy
```

*Deal data from [CheapShark](https://apidocs.cheapshark.com/). Prices may change —
always confirm on the store. Educational/personal project.*
