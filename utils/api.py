import requests
from requests.auth import HTTPBasicAuth
import os
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("OXY_USERNAME")
PASSWORD = os.getenv("OXY_PASSWORD")
OXYLABS_URL = "https://realtime.oxylabs.io/v1/queries"

PLATFORMS = {
    "Amazon": {
        "source": "amazon_search",
        "label": "Amazon",
        "geo_location": "10001",          # Amazon requires US zip code
        "badge_color": "#E47911",
        "text_color": "#FFFFFF",
    },
    "Google Shopping": {
        "source": "google_shopping_search",
        "label": "Google Shopping",
        "geo_location": "United States",
        "badge_color": "#1A73E8",
        "text_color": "#FFFFFF",
    },
    "Flipkart": {
        "source": "flipkart_search",
        "label": "Flipkart",
        "geo_location": "India",          # Flipkart is India-based
        "badge_color": "#2874F0",
        "text_color": "#FFFFFF",
    },
}

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


def _fetch_platform(platform_name, query):
    config = PLATFORMS[platform_name]
    payload = {
        "source": config["source"],
        "query": query,
        "parse": True,
        "geo_location": config["geo_location"],
    }
    try:
        resp = requests.post(
            OXYLABS_URL,
            json=payload,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            timeout=35,
        )
        if resp.status_code == 200:
            return platform_name, resp.json()
        return platform_name, {"_error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
    except Exception as exc:
        return platform_name, {"_error": str(exc)}


def fetch_all_platforms(query):
    results = {}
    with ThreadPoolExecutor(max_workers=len(PLATFORMS)) as executor:
        futures = {executor.submit(_fetch_platform, name, query): name for name in PLATFORMS}
        for future in as_completed(futures):
            platform, data = future.result()
            results[platform] = data
    return results


def _extract_organic(raw):
    """Try every known Oxylabs response path to extract the product list."""
    if not raw or not isinstance(raw, dict):
        return []
    try:
        content = raw["results"][0]["content"]
    except (KeyError, IndexError, TypeError):
        return []

    if isinstance(content, list):
        return content
    if not isinstance(content, dict):
        return []

    results_field = content.get("results", None)
    if isinstance(results_field, dict):
        for key in ("organic", "paid"):
            val = results_field.get(key, [])
            if isinstance(val, list) and val:
                return val
    if isinstance(results_field, list) and results_field:
        return results_field

    for key in ("organic", "items", "products"):
        val = content.get(key, [])
        if isinstance(val, list) and val:
            return val

    return []


def _clean_price(raw):
    if raw is None:
        return 0.0
    if isinstance(raw, (int, float)):
        v = float(raw)
        return v if 0 < v < 1_000_000 else 0.0
    cleaned = "".join(c for c in str(raw) if c.isdigit() or c == ".")
    try:
        v = float(cleaned)
        return v if 0 < v < 1_000_000 else 0.0
    except ValueError:
        return 0.0


def _clean_float(raw):
    try:
        v = float(raw) if raw else 0.0
        return v if 0 < v <= 10 else 0.0
    except (ValueError, TypeError):
        return 0.0


def _clean_int(raw):
    if raw is None:
        return 0
    try:
        return int(str(raw).replace(",", "").split(".")[0].split()[0])
    except (ValueError, IndexError):
        return 0


def _parse_item(item, platform):
    if not isinstance(item, dict):
        return None
    cfg = PLATFORMS[platform]

    price = _clean_price(
        item.get("price") or item.get("price_str") or
        item.get("price_upper") or item.get("min_price")
    )
    rating = _clean_float(item.get("rating") or item.get("score") or item.get("stars"))
    if rating > 5:
        rating = round(rating / 2.0, 1)

    reviews = _clean_int(
        item.get("reviews_count") or item.get("reviews") or
        item.get("ratings_total") or item.get("review_count")
    )
    url = item.get("url") or item.get("link") or item.get("product_url") or ""
    if url and not url.startswith("http"):
        url = "https://" + url

    image = (
        item.get("url_image") or item.get("thumbnail") or
        item.get("image") or item.get("img") or ""
    )
    title = (
        item.get("title") or item.get("name") or item.get("product_name") or ""
    )
    if not title:
        return None

    return {
        "title": str(title).strip(),
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "url": url,
        "image": image,
        "platform": platform,
        "label": cfg["label"],
        "badge_color": cfg["badge_color"],
        "text_color": cfg["text_color"],
        "score": 0.0,
    }


def _parse_platform(platform, raw):
    if not raw or "_error" in raw:
        return []
    organic = _extract_organic(raw)
    return [p for p in (_parse_item(item, platform) for item in organic[:12]) if p]


def _calculate_scores(products):
    valid_prices = [p["price"] for p in products if p["price"] > 0]
    min_p = min(valid_prices) if valid_prices else 0
    max_p = max(valid_prices) if valid_prices else 0

    for p in products:
        r_score  = (p["rating"] / 5.0) * 40 if p["rating"] else 0
        rv_score = min(math.log10(p["reviews"] + 1) / math.log10(100_000) * 30, 30) if p["reviews"] else 0
        if max_p > min_p and p["price"] > 0:
            price_score = (1 - (p["price"] - min_p) / (max_p - min_p)) * 30
        elif p["price"] > 0:
            price_score = 15
        else:
            price_score = 0
        p["score"] = round(r_score + rv_score + price_score, 1)
    return products


def search_electronics(query):
    if not USERNAME or not PASSWORD:
        raise ValueError("OXY_USERNAME / OXY_PASSWORD not set in .env")
    raw_results = fetch_all_platforms(query)
    all_products = []
    errors = {}
    for platform, raw in raw_results.items():
        if raw and "_error" in raw:
            errors[platform] = raw["_error"]
            continue
        all_products.extend(_parse_platform(platform, raw))
    all_products = _calculate_scores(all_products)
    all_products.sort(key=lambda x: x["score"], reverse=True)
    return all_products, errors