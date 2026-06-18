"""
config.py — all the settings for your Game Deals Digest in one place.

Tweak these values; you never need to touch the code. Everything here is read by
the rest of the program. Beginner-friendly: change a number, re-run, see the effect.
"""

# --- The data source: CheapShark (FREE, no API key). https://apidocs.cheapshark.com/ ---
API_BASE = "https://www.cheapshark.com/api/1.0"
USER_AGENT = "GameDealsDigest/1.0 (personal project)"   # APIs like a real User-Agent

# --- How we choose which deals make the digest ---
SORT_BY = "Deal Rating"   # CheapShark's own quality score (blends price, savings, ratings)
MIN_SAVINGS = 30          # only show deals at least this % off
MIN_PRICE = 1.0           # skip $0 "starter pack"/DLC spam (sale price must be >= this)
MAX_PRICE = 40.0          # focus on affordable deals people actually buy
MAX_DEALS = 60            # size of the deal pool we build the sections from
FETCH_PAGE_SIZE = 60      # deals per API page (CheapShark max is 60)
FETCH_PAGES = 6           # how many pages to pull before filtering (more = better choice)

# Quality gate: only feature REAL games with genuine Steam reviews. This is what
# filters out DLC, asset packs, soundtracks, and shovelware.
MIN_STEAM_REVIEWS = 100   # the game must have at least this many Steam reviews
MIN_STEAM_RATING = 70     # ...and at least this % positive

# Only feature deals from these reputable stores (CheapShark store IDs).
# Set to [] to include ALL active stores.
ALLOWED_STORE_IDS = ["1", "7", "8", "11", "13", "15", "25", "27", "35"]
# 1 Steam · 7 GOG · 8 Origin · 11 Humble · 13 Uplay · 15 Fanatical
# 25 Epic · 27 Gamesplanet · 35 Green Man Gaming

# --- Monetisation: your affiliate tags (leave blank until you're approved) ---
# Real affiliate links are per-store; see README. The digest works fine without them.
AFFILIATE = {
    # "Fanatical": "https://www.fanatical.com/...?ref=YOURID",
    # "Green Man Gaming": "...",
}

# --- Output + branding ---
OUTPUT_DIR = "output"
SITE_NAME = "Daily Game Deals"
SITE_TAGLINE = "The best PC game discounts, refreshed every day."
