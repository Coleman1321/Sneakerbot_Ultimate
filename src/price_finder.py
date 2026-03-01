"""
Sneaker Price Finder
--------------------
Searches StockX, GOAT, and eBay for a sneaker SKU and returns
listings sorted by lowest price for a given size.
"""

import re
import time
import logging
import urllib.parse
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json, text/plain, */*",
}


def _new_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


# ---------------------------------------------------------------------------
# Per-platform scrapers
# ---------------------------------------------------------------------------


def _search_stockx(sku: str, size: str, timeout: int = 12) -> List[Dict]:
    """Query the StockX browse endpoint and return normalised result dicts."""
    results: List[Dict] = []
    session = _new_session()
    try:
        params = {
            "productCategory": "sneakers",
            "query": sku,
        }
        resp = session.get(
            "https://stockx.com/api/browse",
            params=params,
            timeout=timeout,
        )
        resp.raise_for_status()
        products = resp.json().get("Products", [])

        for product in products[:6]:
            name = product.get("title", "Unknown")
            url_key = product.get("urlKey", "")
            market = product.get("market", {})
            lowest_ask = market.get("lowestAsk") or market.get("lowestAskFloat")

            if not lowest_ask:
                continue

            # Build per-size URL if size specified
            buy_url = f"https://stockx.com/{url_key}"
            results.append(
                {
                    "platform": "StockX",
                    "name": name,
                    "price": float(lowest_ask),
                    "size": size or "Any",
                    "condition": "New",
                    "url": buy_url,
                    "img": product.get("media", {}).get("thumbUrl", ""),
                }
            )
    except Exception as exc:
        logger.warning("StockX search failed for SKU %r: %s", sku, exc)
    return results


def _search_goat(sku: str, size: str, timeout: int = 12) -> List[Dict]:
    """Query GOAT's Constructor.io-backed search endpoint."""
    results: List[Dict] = []
    session = _new_session()
    try:
        # GOAT uses Constructor.io for search
        ts = int(time.time() * 1000)
        url = (
            f"https://ac.cnstrc.com/search/{urllib.parse.quote(sku)}"
            f"?c=ciojs-client-2.29.5&key=key_XT7bjdbvjgECO5d8"
            f"&i=&s=1&page=1&num_results_per_page=6&_dt={ts}"
        )
        resp = session.get(url, timeout=timeout)
        resp.raise_for_status()
        items = resp.json().get("response", {}).get("results", [])

        for item in items[:6]:
            meta = item.get("data", {})
            price_cents = meta.get("lowest_price_cents_usd") or meta.get(
                "retail_price_cents"
            )
            if not price_cents:
                continue

            slug = meta.get("slug", "")
            img = meta.get("image_url", "")
            results.append(
                {
                    "platform": "GOAT",
                    "name": item.get("value", "Unknown"),
                    "price": price_cents / 100,
                    "size": size or "Any",
                    "condition": "New",
                    "url": f"https://www.goat.com/sneakers/{slug}",
                    "img": img,
                }
            )
    except Exception as exc:
        logger.warning("GOAT search failed for SKU %r: %s", sku, exc)
    return results


def _search_ebay(sku: str, size: str, timeout: int = 15) -> List[Dict]:
    """Scrape eBay BIN (Buy It Now) sneakers listings."""
    results: List[Dict] = []
    query = f"{sku} size {size}".strip() if size else sku
    encoded = urllib.parse.quote(query)
    # _sop=15 = Price + Shipping: lowest first, LH_BIN=1 = Buy It Now only
    url = (
        f"https://www.ebay.com/sch/i.html"
        f"?_nkw={encoded}&_sop=15&_ipg=10&LH_BIN=1&rt=nc&_sacat=15709"
    )
    try:
        headers = {**HEADERS, "Accept": "text/html,application/xhtml+xml"}
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select(".s-item")[:10]:
            title_el = item.select_one(".s-item__title")
            price_el = item.select_one(".s-item__price")
            link_el = item.select_one(".s-item__link")
            img_el = item.select_one(".s-item__image-img")

            if not (title_el and price_el and link_el):
                continue

            title = title_el.get_text(strip=True)
            if "Shop on eBay" in title:
                continue

            price_text = price_el.get_text(strip=True)
            m = re.search(r"\$([0-9,]+\.?\d*)", price_text)
            if not m:
                continue

            price = float(m.group(1).replace(",", ""))
            img = img_el.get("src", "") if img_el else ""
            link = link_el.get("href", "")

            results.append(
                {
                    "platform": "eBay",
                    "name": title[:100],
                    "price": price,
                    "size": size or "See listing",
                    "condition": "Various",
                    "url": link,
                    "img": img,
                }
            )
    except Exception as exc:
        logger.warning("eBay search failed for SKU %r: %s", sku, exc)
    return results


def _search_grailed(sku: str, size: str, timeout: int = 12) -> List[Dict]:
    """Search Grailed via their Algolia-backed API."""
    results: List[Dict] = []
    session = _new_session()
    try:
        query = f"{sku} {size}".strip() if size else sku
        # Grailed's public Algolia app/key
        payload = {
            "requests": [
                {
                    "indexName": "Listing_production",
                    "params": urllib.parse.urlencode(
                        {
                            "query": query,
                            "hitsPerPage": 6,
                            "filters": "sold=0",
                            "attributesToRetrieve": "id,title,price,photos,slug,category",
                        }
                    ),
                }
            ]
        }
        resp = session.post(
            "https://mnrwefss2q-dsn.algolia.net/1/indexes/*/queries"
            "?x-algolia-application-id=MNRWEFSS2Q"
            "&x-algolia-api-key=a776c4563c4d3f65f4a4e0b145f16867",
            json=payload,
            timeout=timeout,
        )
        resp.raise_for_status()
        hits = resp.json().get("results", [{}])[0].get("hits", [])

        for hit in hits[:6]:
            price = hit.get("price")
            if not price:
                continue
            photos = hit.get("photos", {})
            cover = photos.get("cover", {}).get("url", "") if photos else ""
            slug = hit.get("id", "")
            results.append(
                {
                    "platform": "Grailed",
                    "name": hit.get("title", "Unknown")[:100],
                    "price": float(price),
                    "size": size or "Any",
                    "condition": "Used / New",
                    "url": f"https://www.grailed.com/listings/{slug}",
                    "img": cover,
                }
            )
    except Exception as exc:
        logger.warning("Grailed search failed for SKU %r: %s", sku, exc)
    return results


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def find_prices(sku: str, size: str = "") -> List[Dict]:
    """
    Search all configured platforms concurrently and return results
    sorted by price (lowest first).

    Parameters
    ----------
    sku:  The sneaker style code, e.g. ``"DZ5485-612"`` or ``"Yeezy 350 Zebra"``
    size: US men's size string, e.g. ``"10.5"``.  Pass ``""`` to skip filtering.

    Returns
    -------
    List of dicts with keys: platform, name, price, size, condition, url, img
    """
    scrapers = [
        (_search_stockx, "StockX"),
        (_search_goat, "GOAT"),
        (_search_ebay, "eBay"),
        (_search_grailed, "Grailed"),
    ]

    all_results: List[Dict] = []
    with ThreadPoolExecutor(max_workers=len(scrapers)) as pool:
        futures = {
            pool.submit(fn, sku, size): label for fn, label in scrapers
        }
        for future in as_completed(futures):
            label = futures[future]
            try:
                all_results.extend(future.result())
            except Exception as exc:
                logger.warning("Unexpected error from %s: %s", label, exc)

    all_results.sort(key=lambda x: x["price"])
    return all_results
