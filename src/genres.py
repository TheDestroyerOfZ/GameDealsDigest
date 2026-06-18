"""
genres.py — add genre tags to deals.

CheapShark doesn't give us genres, but it gives each game's Steam ID. Steam's free
appdetails API returns genres, so we look them up here. Results are cached to disk
(genres never change) so we don't refetch the same game twice.

Built to FAIL SOFTLY: if Steam is slow, rate-limits, or a game isn't on Steam, that
game simply gets no genres — the site still builds fine.
"""

import json
import os
import time

import requests

import config

_CACHE_PATH = os.path.join(config.OUTPUT_DIR, ".genre_cache.json")
_STEAM_URL = "https://store.steampowered.com/api/appdetails"


def _load_cache():
    if os.path.exists(_CACHE_PATH):
        try:
            with open(_CACHE_PATH) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_cache(cache):
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    with open(_CACHE_PATH, "w") as f:
        json.dump(cache, f)


def _fetch_genres(app_id):
    """Look up a single game's genres on Steam. Returns [] on any failure."""
    try:
        r = requests.get(_STEAM_URL, params={"appids": app_id, "l": "english"},
                         headers={"User-Agent": config.USER_AGENT}, timeout=15)
        entry = r.json().get(str(app_id), {})
        if not entry.get("success"):
            return []
        genres = entry.get("data", {}).get("genres", [])
        # Skip non-descriptive tags; keep up to 3 real genres.
        names = [g["description"] for g in genres
                 if g.get("description") not in ("Free To Play",)]
        return names[:3]
    except Exception:
        return []


def enrich(deals):
    """Add a 'genres' list to each deal (using a disk cache). Fails softly per game."""
    cache = _load_cache()
    changed = False
    for d in deals:
        app_id = d.get("steam_app_id")
        if not app_id:
            continue
        key = str(app_id)
        if key not in cache:
            cache[key] = _fetch_genres(app_id)
            changed = True
            time.sleep(0.25)               # be polite to Steam's API
        d["genres"] = cache.get(key, [])
    if changed:
        _save_cache(cache)
    return deals


def all_genres(deals):
    """The sorted set of every genre present (for building the filter dropdown)."""
    seen = set()
    for d in deals:
        seen.update(d.get("genres", []))
    return sorted(seen)
