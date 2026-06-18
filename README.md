# 🎮 Game Deals Digest

An **automated** daily PC-game-deals site. One scheduled command fetches the best
current deals (from the free CheapShark API — no key, no scraping) and writes a
ready-to-publish web page, blog post, and social captions. Set it up once, and it
updates itself.

This is the *low-maintenance, code-driven* version of the "make money with AI in a
niche" idea: instead of writing content by hand every day, the program writes it.

---

## 🤔 Honest expectations (read this first)

- **The engine runs itself. Getting visitors does not.** Code can't make people show
  up — that's the one part that needs your effort (sharing the page on Pinterest /
  Reddit / a gaming community). It's light, not daily, but it's real.
- **Money is gradual and modest.** Income comes from **affiliate links** (you earn a
  small cut when someone buys through your link) and optionally **display ads**. Both
  need traffic and program approval. Think "slow side income," not "passive jackpot."
- **No fake promises here.** If it were a one-click money printer, nobody would sell
  you a video about it. The honest edge is that *you can automate what others grind by
  hand.*

---

## 🚀 Setup (one time)

```powershell
cd C:\Users\Duncan-PC\Desktop\GameDealsDigest
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## ▶️ Run it

```powershell
.\.venv\Scripts\python.exe run_daily.py
```

This creates an `output/` folder containing:
- **`index.html`** — your website (always the latest deals). Open it in a browser.
- **`deals-YYYY-MM-DD.html`** — a dated archive copy.
- **`deals-YYYY-MM-DD.md`** — a blog post to paste into Blogger / WordPress.
- **`social-YYYY-MM-DD.txt`** — captions to paste on Pinterest / X / Reddit.

## ⚙️ Make it fully automatic (Windows Task Scheduler)

1. Open **Task Scheduler** → *Create Basic Task*.
2. Trigger: **Daily**.
3. Action: **Start a program** →
   - Program: `C:\Users\Duncan-PC\Desktop\GameDealsDigest\.venv\Scripts\python.exe`
   - Arguments: `run_daily.py`
   - Start in: `C:\Users\Duncan-PC\Desktop\GameDealsDigest`
4. Done — it now rebuilds the digest every day on its own.

## 🌐 Publish the page for free

Point any free host at the `output/` folder so the world can see `index.html`:
- **GitHub Pages** (free, great with the daily file) or **Netlify** (drag-and-drop).
- Or paste the daily `.md` into a free **Blogger** blog.

## 💰 Turn on the money (when you're ready)

1. Apply to a store affiliate programme — **Fanatical**, **Green Man Gaming**, and
   **Humble** are good starts for games.
2. Once approved, put your real affiliate link format in `AFFILIATE` in
   [`config.py`](config.py), keyed by the store name. `affiliate.py` will use it
   automatically.
3. (Optional) Add **Google AdSense** to the published page for display-ad income.

## 🛠️ Tweak it

Everything adjustable lives in [`config.py`](config.py): which stores, price range,
minimum discount, how many deals, site name/tagline. Change a value, re-run, done.

## 📁 Project layout

```
GameDealsDigest/
├── config.py          <- all your settings (edit this, not the code)
├── run_daily.py       <- the one command: fetch -> build -> save
├── requirements.txt   <- dependencies (just 'requests')
├── src/
│   ├── stores.py      <- store id -> name (cached)
│   ├── deals.py       <- fetch + clean + de-dupe the deals (data engine)
│   ├── affiliate.py   <- builds the buy link (your money hook)
│   └── digest.py      <- builds the page / blog post / social captions (content engine)
└── output/            <- generated files land here (this is what you publish)
```

*Deal data from [CheapShark](https://apidocs.cheapshark.com/). Educational/personal
project.*
