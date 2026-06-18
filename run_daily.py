"""
run_daily.py — the ONE command that does everything.

    python run_daily.py

It fetches today's best deals, builds the digest (web page + blog post + social
captions), and saves them into the output/ folder. Schedule this once with Windows
Task Scheduler and your site updates itself every day — that's the whole point.
"""

import os
from datetime import date

import config
from src import digest
from src.deals import get_deals


def main():
    print("Fetching today's best game deals...")
    deals = get_deals()
    if not deals:
        print("No deals matched your filters today. Try loosening the limits in config.py.")
        return

    today = date.today().isoformat()
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    files = {
        f"deals-{today}.html": digest.build_html(deals, today),
        "index.html": digest.build_html(deals, today),     # latest always at index.html
        f"deals-{today}.md": digest.build_markdown(deals, today),
        f"social-{today}.txt": digest.build_social(deals, today),
    }
    for name, content in files.items():
        with open(os.path.join(config.OUTPUT_DIR, name), "w", encoding="utf-8") as f:
            f.write(content)

    print(f"[OK] Built a digest of {len(deals)} deals -> {config.OUTPUT_DIR}/index.html")
    print("Top picks today:")
    for d in deals[:5]:
        print(f"  - {d['title']}: ${d['sale_price']:.2f} (-{d['savings_pct']}%) @ {d['store']}")
    print(f"\nOpen {config.OUTPUT_DIR}/index.html in your browser to see the page.")


if __name__ == "__main__":
    main()
