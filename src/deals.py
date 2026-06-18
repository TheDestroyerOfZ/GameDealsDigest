"""
deals.py — the data engine. Fetches current game deals from CheapShark, then
filters them down to a clean, quality, de-duplicated list ready for the digest.
"""

import requests

import config
from src.stores import get_store_map


def _fetch_raw():
    """Pull several pages of deals from the API, sorted by quality."""
    deals = []
    for page in range(config.FETCH_PAGES):
        params = {"sortBy": config.SORT_BY, "desc": 1,
                  "pageSize": config.FETCH_PAGE_SIZE, "pageNumber": page}
        resp = requests.get(f"{config.API_BASE}/deals", params=params,
                            headers={"User-Agent": config.USER_AGENT}, timeout=25)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        deals.extend(batch)
    return deals


def _to_int(value):
    """Best-effort int conversion (yfinance/CheapShark sometimes send strings/None)."""
    try:
        return int(value or 0)
    except (ValueError, TypeError):
        return 0


def _is_real_game(d):
    """Keep only games with genuine Steam reviews — filters out DLC/asset-pack spam."""
    try:
        reviews = int(d.get("steamRatingCount") or 0)
        rating = int(d.get("steamRatingPercent") or 0)
    except (ValueError, TypeError):
        return False
    return reviews >= config.MIN_STEAM_REVIEWS and rating >= config.MIN_STEAM_RATING


def get_deals():
    """Return a cleaned list of the best deals (de-duplicated, keeping the cheapest)."""
    stores = get_store_map()
    allowed = set(config.ALLOWED_STORE_IDS) or set(stores)
    raw = _fetch_raw()

    cleaned, seen = [], {}     # seen: lowercase title -> index in cleaned (for de-dupe)
    for d in raw:
        if d.get("storeID") not in allowed:
            continue
        if not _is_real_game(d):
            continue
        try:
            sale = float(d["salePrice"])
            normal = float(d["normalPrice"])
            savings = float(d["savings"])
        except (KeyError, ValueError, TypeError):
            continue
        if sale < config.MIN_PRICE or sale > config.MAX_PRICE or savings < config.MIN_SAVINGS:
            continue
        title = (d.get("title") or "").strip()
        if not title:
            continue

        try:
            meta = int(d.get("metacriticScore") or 0)
        except (ValueError, TypeError):
            meta = 0
        item = {
            "title": title,
            "sale_price": round(sale, 2),
            "normal_price": round(normal, 2),
            "savings_pct": round(savings),
            "store": stores.get(d.get("storeID"), "Unknown"),
            "deal_id": d.get("dealID"),
            "thumb": d.get("thumb"),
            "steam_pct": d.get("steamRatingPercent"),
            "steam_reviews": _to_int(d.get("steamRatingCount")),
            "metacritic": meta if meta > 0 else None,
        }
        key = title.lower()
        if key in seen:                                    # same game, another store
            if item["sale_price"] < cleaned[seen[key]]["sale_price"]:
                cleaned[seen[key]] = item                  # keep the cheaper one
        else:
            seen[key] = len(cleaned)
            cleaned.append(item)

    return cleaned[:config.MAX_DEALS]                       # already quality-sorted by the API


def sections(pool, per_section=8):
    """
    Split the deal pool into themed sections for a richer page. A game can appear in
    more than one section (e.g. both a big discount AND top rated) — that's normal.
    """
    by_rating = sorted((d for d in pool if d.get("steam_pct")),
                       key=lambda d: -int(d["steam_pct"]))
    by_savings = sorted(pool, key=lambda d: -d["savings_pct"])
    by_popular = sorted(pool, key=lambda d: -(d.get("steam_reviews") or 0))
    budget = sorted((d for d in pool if d["sale_price"] <= 5),
                    key=lambda d: -d["savings_pct"])
    out = [
        # Lead with the most-reviewed (= most recognizable) games for a strong first impression.
        {"title": "🎮 Today's Best Deals", "deals": by_popular[:per_section]},
        {"title": "🔥 Biggest Discounts", "deals": by_savings[:per_section]},
        {"title": "⭐ Top Rated", "deals": by_rating[:per_section]},
    ]
    if budget:
        out.append({"title": "💸 Under $5", "deals": budget[:per_section]})
    return [s for s in out if s["deals"]]
