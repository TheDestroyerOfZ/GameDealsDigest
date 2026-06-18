"""
run_daily.py — the ONE command that does everything.

    python run_daily.py

It fetches today's best deals, builds the digest (web page + blog post + social
captions), and saves them into the output/ folder. Schedule this once with Windows
Task Scheduler and your site updates itself every day — that's the whole point.
"""

import os
import sys
from datetime import date

# Windows consoles default to cp1252 and choke on emoji in our section titles;
# force UTF-8 so local runs print cleanly. (GitHub Actions/Linux is already UTF-8.)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import config
from src import digest
from src.deals import get_deals, sections


def main():
    print("Fetching today's best game deals...")
    pool = get_deals()
    if not pool:
        print("No deals matched your filters today. Try loosening the limits in config.py.")
        return

    secs = sections(pool)
    today = date.today().isoformat()
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    html = digest.build_html(secs, today, pool)
    files = {
        f"deals-{today}.html": html,
        "index.html": html,                                # latest always at index.html
        f"deals-{today}.md": digest.build_markdown(pool, today),
        f"social-{today}.txt": digest.build_social(pool, today),
    }
    for name, content in files.items():
        with open(os.path.join(config.OUTPUT_DIR, name), "w", encoding="utf-8") as f:
            f.write(content)

    print(f"[OK] Built a {len(pool)}-deal page in {len(secs)} sections -> {config.OUTPUT_DIR}/index.html")
    for s in secs:
        print(f"  {s['title']}: {len(s['deals'])} deals")
    print(f"\nOpen {config.OUTPUT_DIR}/index.html in your browser to see the page.")


if __name__ == "__main__":
    main()
