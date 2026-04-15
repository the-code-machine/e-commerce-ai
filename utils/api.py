import requests
from requests.auth import HTTPBasicAuth
import os
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("OXY_USERNAME")
PASSWORD = os.getenv("OXY_PASSWORD")
OXYLABS_URL = "https://realtime.oxylabs.io/v1/queries"

# ── Platform registry ────────────────────────────────────────────────────────
PLATFORMS = {
    "Amazon": {
        "source": "amazon_search",
        "icon": "🛒",
        "badge_color": "#FF9900",
        "badge_text": "#000000",
        "bg": "#FFF8EC",
    },
    "Google Shopping": {
        "source": "google_shopping_search",
        "icon": "🛍️",
        "badge_color": "#4285F4",
        "badge_text": "#FFFFFF",
        "bg": "#EEF4FF",
    },
    "Flipkart": {
        "source": "flipkart_search",
        "icon": "📦",
        "badge_color": "#2874F0",
        "badge_text": "#FFFFFF",
        "bg": "#EEF2FF",
    },
}

# ── Category → search hint ────────────────────────────────────────────────────
CATEGORY_HINTS = {
    "Smartphones & Mobiles": "smartphone",
    "Laptops & Computers": "laptop",
    "Headphones & Audio": "headphones",
    "Cameras & Photography": "digital camera",
    "Smart Watches": "smartwatch",
    "Tablets": "tablet",
    "TVs & Displays": "4K television",
    "Gaming": "gaming console",
    "Smart Home": "smart home device",
    "All Electronics": "",
}


# ── Raw fetch ─────────────────────────────────────────────────────────────────
def _fetch_platform(platform_name: str, query: str) -> tuple:
    config = PLATFORMS[platform_name]
    payload = {
        "source": config["source"],
        "query": query,
        "parse": True,
        "geo_location": "United States",
    }
    try:
        resp = requests.post(
            OXYLABS_URL,
            json=payload,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            timeout=30,
        )
        if resp.status_code == 200:
            return platform_name, resp.json()
        return platform_name, {"_error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
    except Exception as exc:
        return platform_name, {"_error": str(exc)}


def fetch_all_platforms(query: str) -> dict:
    """Fetch all platforms in parallel. Returns {platform: raw_data}."""
    results = {}
    with ThreadPoolExecutor(max_workers=len(PLATFORMS)) as executor:
        futures = {
            executor.submit(_fetch_platform, name, query): name
            for name in PLATFORMS
        }
        for future in as_completed(futures):
            platform, data = future.result()
            results[platform] = data
    return results


# ── Parser ────────────────────────────────────────────────────────────────────
def _clean_price(raw) -> float:
    if raw is None:
        return 0.0
    if isinstance(raw, (int, float)):
        return float(raw)
    cleaned = "".join(c for c in str(raw) if c.isdigit() or c == ".")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _clean_int(raw) -> int:
    if raw is None:
        return 0
    try:
        return int(str(raw).replace(",", "").replace(".", "").split()[0])
    except (ValueError, IndexError):
        return 0


def _parse_platform(platform: str, raw: dict) -> list:
    """Normalise a platform's raw API response into a list of product dicts."""
    if not raw or "_error" in raw:
        return []

    products = []
    try:
        organic = (
            raw["results"][0]["content"]
            .get("results", {})
            .get("organic", [])
        )
    except (KeyError, IndexError, TypeError):
        return products

    cfg = PLATFORMS[platform]

    for item in organic[:12]:
        price = _clean_price(
            item.get("price") or item.get("price_str") or item.get("price_upper")
        )
        rating = 0.0
        try:
            rating = float(item.get("rating") or item.get("score") or 0)
        except (ValueError, TypeError):
            pass

        reviews = _clean_int(
            item.get("reviews_count") or item.get("reviews") or item.get("ratings_total")
        )

        url = item.get("url") or item.get("link") or ""
        if url and not url.startswith("http"):
            url = "https://" + url

        image = (
            item.get("url_image")
            or item.get("thumbnail")
            or item.get("image")
            or ""
        )

        # bullet_points can be a list OR a single string — handle both
        raw_bullets = item.get("bullet_points", [])
        if isinstance(raw_bullets, str):
            bullets = [raw_bullets] if raw_bullets.strip() else []
        elif isinstance(raw_bullets, list):
            bullets = [b for b in raw_bullets if isinstance(b, str) and len(b) > 1]
        else:
            bullets = []

        products.append(
            {
                "title": item.get("title", "Unknown Product"),
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "url": url,
                "image": image,
                "bullets": bullets,
                "platform": platform,
                "icon": cfg["icon"],
                "badge_color": cfg["badge_color"],
                "badge_text": cfg["badge_text"],
                "bg": cfg["bg"],
                "score": 0.0,  # filled later
            }
        )

    return products


# ── Scoring ───────────────────────────────────────────────────────────────────
def _calculate_scores(products: list) -> list:
    """
    Score (0–100) = Rating(40) + Reviews(30) + Price-value(30).
    Lower price vs. pool → higher price score.
    """
    valid_prices = [p["price"] for p in products if p["price"] > 0]
    min_p = min(valid_prices) if valid_prices else 0
    max_p = max(valid_prices) if valid_prices else 0

    for p in products:
        # 40 pts — rating
        r_score = (p["rating"] / 5.0) * 40 if p["rating"] else 0

        # 30 pts — review count (log-scaled, 100k = full marks)
        rv_score = min(math.log10(p["reviews"] + 1) / math.log10(100_000) * 30, 30) if p["reviews"] else 0

        # 30 pts — price (lower = better)
        if max_p > min_p and p["price"] > 0:
            price_score = (1 - (p["price"] - min_p) / (max_p - min_p)) * 30
        elif p["price"] > 0:
            price_score = 30
        else:
            price_score = 0

        p["score"] = round(r_score + rv_score + price_score, 1)

    return products


# ── Public API ────────────────────────────────────────────────────────────────
def search_electronics(query: str) -> tuple:
    """
    Returns (products_sorted_by_score, platform_errors).
    """
    if not USERNAME or not PASSWORD:
        raise ValueError("OXY_USERNAME / OXY_PASSWORD not set in .env")

    raw_results = fetch_all_platforms(query)

    all_products: list = []
    errors: dict = {}

    for platform, raw in raw_results.items():
        if raw and "_error" in raw:
            errors[platform] = raw["_error"]
        parsed = _parse_platform(platform, raw)
        all_products.extend(parsed)

    all_products = _calculate_scores(all_products)
    all_products.sort(key=lambda x: x["score"], reverse=True)

    return all_products, errors