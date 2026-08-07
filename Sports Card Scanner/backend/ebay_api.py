"""Real eBay Buy API integration -- an upgrade path over enrich.py's
general-web-search-steered-at-eBay approach, for accounts with eBay
Developer Program credentials.

Two eBay Buy APIs are used:
- **Browse API** -- search ACTIVE listings. Generally available to any
  registered eBay developer application, no special approval needed. Used
  to get real listing titles/prices/conditions for the card-detail lookup
  (card_number/team/parallel_insert_type) instead of general web search.
- **Marketplace Insights API** -- search recently SOLD listings.
  Historically gated behind a separate approval step in eBay's developer
  program -- **check your application's details on developer.ebay.com to
  confirm you actually have it enabled** before assuming this path works
  for you. Treated as best-effort here: ANY failure (not enabled, 403/404,
  an unexpected response shape) is treated identically to "not available,"
  and callers (enrich.py) fall back to the existing Claude-web-search
  sold-price estimate. This module never raises for that case.

Auth: OAuth 2.0 client-credentials grant (an "Application access token"),
no per-user login needed -- this only ever searches public listing data,
never touches a specific eBay account. Configure in
Sports Card Scanner/.env (same file as ANTHROPIC_API_KEY):
    EBAY_CLIENT_ID=<your App ID / Client ID>
    EBAY_CLIENT_SECRET=<your Cert ID / Client Secret>
    EBAY_ENV=production   # or "sandbox"; defaults to production
Get these from your application's keys on developer.ebay.com. Use your
**production** keys for this to search real listings -- sandbox only has
eBay's fake test data (useful for confirming the integration itself talks
to eBay correctly, not for real card research).

If EBAY_CLIENT_ID/EBAY_CLIENT_SECRET aren't set, every function here
returns None immediately and enrich.py's existing Claude-web-search path
runs unchanged -- this is purely additive, nothing breaks without it.

Caveat, same spirit as enrich.py's WEB_SEARCH_TOOL_TYPE note: the exact
Marketplace Insights response shape reflects what was known at build time
(a v1_beta endpoint at that) -- if eBay has changed it, search_sold_listings
below is written to treat an unrecognized shape as "unavailable" (returns
None) rather than guessing, so it fails soft into the existing fallback
instead of silently returning wrong data.
"""
import base64
import os
import time

import requests

CLIENT_ID = os.environ.get("EBAY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("EBAY_CLIENT_SECRET")
ENV = os.environ.get("EBAY_ENV", "production")
MARKETPLACE_ID = os.environ.get("EBAY_MARKETPLACE_ID", "EBAY_US")

_HOST = "api.sandbox.ebay.com" if ENV == "sandbox" else "api.ebay.com"
TOKEN_URL = f"https://{_HOST}/identity/v1/oauth2/token"
BROWSE_SEARCH_URL = f"https://{_HOST}/buy/browse/v1/item_summary/search"
MARKETPLACE_INSIGHTS_URL = f"https://{_HOST}/buy/marketplace_insights/v1_beta/item_sales/search"

_token_cache = {"token": None, "expires_at": 0.0}


def configured() -> bool:
    return bool(CLIENT_ID and CLIENT_SECRET)


def _get_token() -> str | None:
    """Cached OAuth client-credentials token. Returns None on any failure
    -- callers must treat that the same as "not configured", never raise."""
    if not configured():
        return None
    if _token_cache["token"] and time.time() < _token_cache["expires_at"] - 60:
        return _token_cache["token"]

    creds = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    try:
        resp = requests.post(
            TOKEN_URL,
            headers={
                "Authorization": f"Basic {creds}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope",
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException:
        return None

    token = data.get("access_token")
    if not token:
        return None
    _token_cache["token"] = token
    _token_cache["expires_at"] = time.time() + data.get("expires_in", 7200)
    return token


def _get(url: str, params: dict) -> dict | None:
    token = _get_token()
    if not token:
        return None
    try:
        resp = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "X-EBAY-C-MARKETPLACE-ID": MARKETPLACE_ID,
            },
            params=params,
            timeout=15,
        )
        if resp.status_code != 200:
            return None
        return resp.json()
    except requests.RequestException:
        return None


def _price_value(price_obj: dict | None) -> float | None:
    if not price_obj or price_obj.get("value") is None:
        return None
    try:
        return float(price_obj["value"])
    except (TypeError, ValueError):
        return None


def search_active_listings(query: str, limit: int = 25) -> list[dict] | None:
    """Real ACTIVE eBay listings via the Browse API. Returns a list of
    {"title", "price", "currency", "condition", "url"} dicts, or None if
    unavailable (not configured, auth failure, network error, non-200)."""
    data = _get(BROWSE_SEARCH_URL, {"q": query, "limit": limit})
    if data is None:
        return None
    items = data.get("itemSummaries")
    if items is None:
        return None
    return [
        {
            "title": item.get("title"),
            "price": _price_value(item.get("price")),
            "currency": (item.get("price") or {}).get("currency"),
            "condition": item.get("condition"),
            "url": item.get("itemWebUrl"),
        }
        for item in items
    ]


def search_sold_listings(query: str, limit: int = 25) -> list[dict] | None:
    """Real SOLD eBay listings via the Marketplace Insights API, if your
    application has that API enabled (see module docstring -- not every
    account does). Returns the same shape as search_active_listings plus
    "sold_date", or None if unavailable for ANY reason -- not enabled for
    your app, not configured, auth failure, or a response shape this
    wasn't written against. Callers should silently fall back to another
    approach; None here is not an error worth surfacing to the user."""
    data = _get(MARKETPLACE_INSIGHTS_URL, {"q": query, "limit": limit})
    if data is None:
        return None
    items = data.get("itemSales")
    if items is None:
        # Either genuinely no results, or (more likely) this account
        # doesn't have Marketplace Insights enabled and got a differently
        # shaped response. Either way, treat as unavailable rather than
        # guessing at a shape we haven't confirmed.
        return None
    results = []
    for item in items:
        price_obj = item.get("lastSoldPrice") or item.get("price")
        results.append(
            {
                "title": item.get("title"),
                "price": _price_value(price_obj),
                "currency": (price_obj or {}).get("currency"),
                "condition": item.get("condition"),
                "url": item.get("itemWebUrl"),
                "sold_date": item.get("lastSoldDate") or item.get("soldDate"),
            }
        )
    return results or None
