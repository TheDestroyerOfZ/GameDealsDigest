# CLAUDE.md — Game Deals Digest

Project context for AI coding assistants (and contributors). Read this first.

## What this project is
An automated daily PC game-deals site. `run_daily.py` pulls current deals from the free
CheapShark API (no key, no scraping), filters to quality real games, enriches genres from
Steam, and generates a publishable web page (plus a blog-post markdown file and social
captions). Low-maintenance: run it on a schedule and it updates itself.

## How it works (architecture)
- `config.py` — all settings (stores, price range, min discount, quality gate, affiliate
  tags, branding). Edit this, not the code.
- `run_daily.py` — the one command: fetch → enrich genres → build → save to `output/`.
- `src/stores.py` — store ID → name map (cached).
- `src/deals.py` — fetch (paginated) + filter + de-dupe. Quality gate: only real games
  with ≥100 Steam reviews & ≥70% positive (filters out DLC/asset-pack spam).
- `src/genres.py` — adds genres via Steam's appdetails API (cached; fails softly).
- `src/affiliate.py` — builds the buy link (CheapShark redirect by default; real affiliate
  deep links go in `config.AFFILIATE` once approved).
- `src/digest.py` — content engine: curated highlight sections + a Browse-All grid with
  client-side search/genre/store/price/sort, plus markdown + social captions.
- `output/` — generated files (`index.html` is the latest). This is what gets published.
- `.github/workflows/daily.yml` — GitHub Actions: rebuilds + deploys to Pages daily.

## How to run / test
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_daily.py
```
Notes:
- Windows PowerShell 5.1's old TLS defaults make raw API calls 400; Python `requests`
  is fine, so test through the script, not Invoke-RestMethod.
- The console can choke on emoji in `print()` (cp1252) — `run_daily.py` reconfigures
  stdout to UTF-8 to handle it. Generated files are always written UTF-8.

## Conventions
- Keep code beginner-friendly and well-commented; settings live in `config.py`.
- Keep all captions/disclaimers honest (prices may change; some links may be affiliate
  links). The footer carries the price disclaimer + affiliate disclosure + CheapShark
  attribution.
- Monetisation is affiliate-first (tech audiences block ads). Steam has no affiliate
  program; commissions come from third-party stores (Fanatical/GMG/Humble), which are
  often cheaper than Steam anyway.
