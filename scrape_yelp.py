"""
Scrape restaurants within 0.5 miles of UIUC Siebel Center.
Step 1: Yelp Fusion API  -> business list + metadata
Step 2: Yelp web page   -> review text (BeautifulSoup)
Output: documents/restaurant_<slug>.txt
"""

import os
import re
import time
import json
import math
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

YELP_API_KEY = os.getenv("YELP_API_KEY")
API_HEADERS = {"Authorization": f"Bearer {YELP_API_KEY}"}

WEB_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

CENTER_LAT = 40.1138
CENTER_LON = -88.2249
MAX_MILES = 0.5
RADIUS_METERS = 800   # ~0.5 miles for API search
OUTPUT_DIR = "documents"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def haversine_miles(lat1, lon1, lat2, lon2):
    R = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def api_get(url, params=None, retries=4):
    delay = 2.0
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=API_HEADERS, params=params, timeout=15)
            if resp.status_code == 429:
                time.sleep(delay * (2 ** attempt))
                continue
            resp.raise_for_status()
            return resp
        except requests.exceptions.ConnectionError:
            if attempt < retries - 1:
                time.sleep(delay * (2 ** attempt))
            else:
                raise


def search_restaurants(offset=0):
    resp = api_get(
        "https://api.yelp.com/v3/businesses/search",
        params={
            "latitude": CENTER_LAT,
            "longitude": CENTER_LON,
            "radius": RADIUS_METERS,
            "categories": "restaurants,coffee,food",
            "sort_by": "distance",
            "limit": 50,
            "offset": offset,
        },
    )
    return resp.json()


def get_api_details(biz_id):
    try:
        resp = api_get(f"https://api.yelp.com/v3/businesses/{biz_id}")
        return resp.json()
    except Exception:
        return {}


def scrape_yelp_reviews(yelp_url):
    """Scrape review text from a Yelp business page."""
    try:
        # strip tracking params from URL
        clean_url = yelp_url.split("?")[0]
        resp = requests.get(clean_url, headers=WEB_HEADERS, timeout=20)
        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.text, "lxml")

        # Method 1: look for embedded JSON (Next.js __NEXT_DATA__)
        next_data = soup.find("script", id="__NEXT_DATA__")
        if next_data:
            try:
                data = json.loads(next_data.string)
                reviews = []
                # walk the JSON tree looking for review text
                def find_reviews(obj, depth=0):
                    if depth > 10:
                        return
                    if isinstance(obj, dict):
                        if "text" in obj and "rating" in obj and isinstance(obj["text"], str) and len(obj["text"]) > 30:
                            reviews.append(obj["text"].strip())
                        for v in obj.values():
                            find_reviews(v, depth + 1)
                    elif isinstance(obj, list):
                        for item in obj:
                            find_reviews(item, depth + 1)
                find_reviews(data)
                if reviews:
                    return reviews[:5]
            except Exception:
                pass

        # Method 2: look for review paragraphs in HTML
        review_texts = []

        # Common Yelp review selectors
        for selector in [
            "p.comment__373c0__Nsutg",
            "[class*='comment__']",
            "[class*='review-content']",
            "span.raw__373c0__3rcx7",
        ]:
            nodes = soup.select(selector)
            for node in nodes:
                text = node.get_text(strip=True)
                if len(text) > 50:
                    review_texts.append(text)
            if review_texts:
                break

        # Method 3: find all <p> tags inside likely review containers
        if not review_texts:
            for div in soup.find_all("div", attrs={"data-testid": re.compile(r"review", re.I)}):
                p = div.find("p")
                if p:
                    text = p.get_text(strip=True)
                    if len(text) > 50:
                        review_texts.append(text)

        return review_texts[:5]

    except Exception as e:
        return []


def format_hours(detail):
    try:
        hours_list = detail["hours"][0]["open"]
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        lines = []
        for h in hours_list:
            day = days[h["day"]]
            start = h["start"][:2] + ":" + h["start"][2:]
            end = h["end"][:2] + ":" + h["end"][2:]
            lines.append(f"{day}: {start}-{end}")
        return ", ".join(lines)
    except Exception:
        return "N/A"


def useful_tags(biz, detail):
    tags = []
    price = biz.get("price", "")
    rating = biz.get("rating", 0)

    if price in ("$", "$$"):
        tags.append("Cheap food")
    if rating >= 4.0:
        tags.append("Highly rated")

    cat_aliases = {c["alias"] for c in biz.get("categories", [])}

    if any(a in cat_aliases for a in ["coffee", "cafes", "tea"]):
        tags.append("Coffee / cafe")
    if any(a in cat_aliases for a in ["chinese", "korean", "japanese", "thai", "vietnamese",
                                       "asianfusion", "taiwanese", "ramen", "sushi"]):
        tags.append("Asian food")
    if any(a in cat_aliases for a in ["mexican", "tacos", "burrito"]):
        tags.append("Mexican food")
    if any(a in cat_aliases for a in ["pizza"]):
        tags.append("Pizza")
    if any(a in cat_aliases for a in ["sandwiches", "delis", "wraps"]):
        tags.append("Sandwiches")
    if any(a in cat_aliases for a in ["desserts", "icecream", "bubbletea", "shavedice"]):
        tags.append("Dessert")
    if any(a in cat_aliases for a in ["breakfast_brunch"]):
        tags.append("Breakfast / brunch")

    transactions = biz.get("transactions", [])
    if "pickup" in transactions or "delivery" in transactions:
        tags.append("Takeout / delivery")

    try:
        hours_list = detail.get("hours", [{}])[0].get("open", [])
        for h in hours_list:
            end_h = int(h["end"][:2])
            if end_h >= 22 or (end_h < 6 and h.get("is_overnight")):
                tags.append("Late night")
                break
    except Exception:
        pass

    tags.append("Quick lunch near CS")
    return tags


def slugify(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")[:50]


def write_document(biz, detail, reviews, dist_miles):
    name = biz["name"]
    address = ", ".join(biz["location"].get("display_address", []))
    categories = ", ".join(c["title"] for c in biz.get("categories", []))
    rating = biz.get("rating", "N/A")
    review_count = biz.get("review_count", "N/A")
    price = biz.get("price", "N/A") or "N/A"
    phone = biz.get("display_phone", "N/A")
    yelp_url = biz.get("url", "N/A").split("?")[0]
    hours_str = format_hours(detail)
    tags = useful_tags(biz, detail)

    snippets_block = (
        "\n".join(f'- "{r}"' for r in reviews)
        if reviews
        else "- (No review snippets available)"
    )
    tag_lines = "\n".join(f"- {t}" for t in tags)

    doc = f"""Title: {name} Review Profile
Source: Yelp
Source URL: {yelp_url}
Date Collected: 2026-06-07
Reference Location: Siebel Center for Computer Science, UIUC

== METADATA ==
Restaurant: {name}
Address: {address}
Distance from Siebel Center: {dist_miles:.2f} miles
Categories: {categories}
Rating: {rating} / 5.0
Review Count: {review_count}
Price Level: {price}
Phone: {phone}
Opening Hours: {hours_str}

== REVIEW SNIPPETS ==
{snippets_block}

== USEFUL FOR ==
{tag_lines}
"""

    filename = f"restaurant_{slugify(name)}.txt"
    base = filename[:-4]
    count = 1
    while os.path.exists(os.path.join(OUTPUT_DIR, filename)):
        filename = f"{base}_{count}.txt"
        count += 1

    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(doc.strip())
    return filename


def main():
    print("Step 1: Fetching restaurant list from Yelp API...")
    seen_ids = set()
    all_businesses = []

    for offset in [0, 50]:
        data = search_restaurants(offset=offset)
        for biz in data.get("businesses", []):
            if biz["id"] not in seen_ids:
                coords = biz.get("coordinates", {})
                lat = coords.get("latitude", CENTER_LAT)
                lon = coords.get("longitude", CENTER_LON)
                dist = haversine_miles(CENTER_LAT, CENTER_LON, lat, lon)
                if dist <= MAX_MILES:
                    biz["_dist"] = dist
                    seen_ids.add(biz["id"])
                    all_businesses.append(biz)
        if len(data.get("businesses", [])) < 50:
            break
        time.sleep(1.5)

    all_businesses.sort(key=lambda b: b["_dist"])
    print(f"Found {len(all_businesses)} restaurants within 0.5 miles.\n")

    print("Step 2: Fetching details + scraping reviews...")
    success = 0
    for i, biz in enumerate(all_businesses):
        name = biz["name"]
        dist = biz["_dist"]
        yelp_url = biz.get("url", "")

        detail = get_api_details(biz["id"])
        time.sleep(1.0)

        reviews = []
        if yelp_url:
            reviews = scrape_yelp_reviews(yelp_url)
            time.sleep(2.5)  # polite delay between web requests

        fname = write_document(biz, detail, reviews, dist)
        review_note = f"{len(reviews)} snippets" if reviews else "no snippets"
        print(f"  [{i+1}/{len(all_businesses)}] {name} ({dist:.2f} mi) -> {fname} [{review_note}]")
        success += 1

    print(f"\nDone. {success} files written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
