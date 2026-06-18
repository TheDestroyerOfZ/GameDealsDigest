"""
currency.py — live exchange rates so visitors can switch currency.

CheapShark prices are in USD. We fetch USD -> each configured currency from the free
Frankfurter API (ECB rates, no key) and the page converts prices in the browser.

IMPORTANT: converted prices are APPROXIMATIONS — a straight FX conversion is NOT the
store's actual regional price. The page says so. Fails softly to USD-only if the rate
lookup fails.
"""

import requests

import config

_URL = "https://api.frankfurter.app/latest"


def get_rates():
    """Return {currency_code: rate_from_USD}. Always includes USD=1.0; fails soft."""
    rates = {"USD": 1.0}
    targets = [c for c in config.CURRENCIES if c != "USD"]
    if not targets:
        return rates
    try:
        r = requests.get(_URL, params={"from": "USD", "to": ",".join(targets)},
                         headers={"User-Agent": config.USER_AGENT}, timeout=15)
        data = r.json().get("rates", {})
        for c in targets:
            if c in data:
                rates[c] = round(float(data[c]), 4)
    except Exception:
        pass                                  # USD-only is a fine fallback
    return rates
