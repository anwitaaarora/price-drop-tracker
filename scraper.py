import re
import requests
from bs4 import BeautifulSoup


def scrape_product_info(url):
    """Fetches web content and parses price and availability using BeautifulSoup."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[-] Error fetching URL: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract price with fallback matching
    price_element = soup.find(class_=re.compile(r"price|amount|val", re.I))
    if not price_element:
        price_element = soup.find(string=re.compile(r"[\$₹€]\s*\d+"))

    if price_element:
        price_raw = (
            price_element.get_text()
            if hasattr(price_element, "get_text")
            else str(price_element)
        )
        cleaned_price = re.sub(r"[^\d.]", "", price_raw.replace(",", ""))
        try:
            current_price = float(cleaned_price)
        except ValueError:
            current_price = None
    else:
        current_price = None

    page_text = soup.get_text().lower()
    is_in_stock = "out of stock" not in page_text and "sold out" not in page_text

    return {"price": current_price, "is_in_stock": is_in_stock}
