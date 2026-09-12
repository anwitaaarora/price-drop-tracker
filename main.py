import time
from database import get_all_products, update_product_price
from plyer import notification
from scraper import scrape_product_info


def send_alert(product_name, current_price, target_price, url):
    """Fires desktop pop-up notification."""
    notification.notify(
        title="🚨 Price Drop Alert!",
        message=f"{product_name} is now ₹{current_price}! (Target: ₹{target_price})",
        app_name="Price Tracker",
        timeout=10,
    )
    print(
        f"[!] ALERT SENT for {product_name}: Current ({current_price}) <= Target ({target_price})"
    )


def run_tracker():
    print("\n[=] Running Price Tracker Check...")
    products = get_all_products()

    if not products:
        print("[-] No products found in database to track.")
        return

    for item in products:
        product_id = item["product_id"]
        name = item["name"]
        url = item["url"]
        target_price = float(item["target_price"])

        print(f"[*] Checking: {name}...")
        scraped_data = scrape_product_info(url)

        if scraped_data and scraped_data["price"] is not None:
            current_price = scraped_data["price"]
            is_in_stock = scraped_data["is_in_stock"]

            update_product_price(product_id, current_price, is_in_stock)
            print(
                f"    -> Current Price: {current_price} | In Stock: {is_in_stock}"
            )

            if current_price <= target_price:
                send_alert(name, current_price, target_price, url)
        else:
            print(f"    [-] Could not extract price for {name}.")


if __name__ == "__main__":
    run_tracker()
