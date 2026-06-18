"""
affiliate.py — builds the "See deal" link for each game.

By default we use CheapShark's redirect link, which always works with no key and
sends the buyer to the right store. THIS IS WHERE YOUR MONEY HOOK GOES: once you're
approved for a store's affiliate programme (Fanatical, Green Man Gaming, etc.), real
affiliate links are store-specific deep links — see README for how to wire them in.
The digest is fully functional before you ever add one.
"""

import config


def deal_link(deal):
    """Return the clickable link for a deal (affiliate-tagged if you've configured it)."""
    tag = config.AFFILIATE.get(deal["store"])
    if tag:
        return tag        # your real affiliate deep link for this store
    return f"https://www.cheapshark.com/redirect?dealID={deal['deal_id']}"
