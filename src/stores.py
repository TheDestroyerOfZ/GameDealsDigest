"""
stores.py — look up the list of game stores (so we can show "Steam", "GOG", etc.
instead of a number). Fetched once from CheapShark and cached on disk.
"""

import json
import os

import requests

import config

_CACHE = os.path.join(config.OUTPUT_DIR, ".stores_cache.json")


def get_store_map():
    """Return {storeID: storeName} for active stores. Cached so we don't refetch."""
    if os.path.exists(_CACHE):
        try:
            with open(_CACHE) as f:
                return json.load(f)
        except Exception:
            pass  # cache unreadable — just refetch below

    resp = requests.get(f"{config.API_BASE}/stores",
                        headers={"User-Agent": config.USER_AGENT}, timeout=25)
    resp.raise_for_status()
    stores = {s["storeID"]: s["storeName"] for s in resp.json() if s.get("isActive")}

    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    with open(_CACHE, "w") as f:
        json.dump(stores, f)
    return stores
