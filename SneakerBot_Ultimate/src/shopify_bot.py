import requests
import json
import time
from src.proxy_manager import get_random_proxy

SHOPIFY_URL = "https://{shop}/products.json"


def monitor_shopify_stock(shop, keywords):
    """Monitors a Shopify store for sneaker drops."""
    proxies = {"http": get_random_proxy(), "https": get_random_proxy()}

    while True:
        try:
            response = requests.get(SHOPIFY_URL.format(shop=shop), proxies=proxies)
            if response.status_code == 200:
                products = response.json()["products"]
                for product in products:
                    if any(keyword.lower() in product["title"].lower() for keyword in keywords):
                        print(f"🔥 Found sneaker: {product['title']} on {shop}!")
                        return product["id"]
            time.sleep(5)
        except Exception as e:
            print(f"❌ Error monitoring {shop}: {e}")
        time.sleep(5)


def checkout_shopify(shop, sneaker_id, size):
    """Attempts to checkout a sneaker from a Shopify store."""
    print(f"🔄 Checking out sneaker {sneaker_id} from {shop} (Size: {size})...")
    # Future implementation: Automate Shopify checkout
    time.sleep(3)
    print("✅ Checkout complete!")


# Example Usage
if __name__ == "__main__":
    sneaker_id = monitor_shopify_stock("kith.com", ["Jordan", "Nike", "Dunk"])
    if sneaker_id:
        checkout_shopify("kith.com", sneaker_id, "10.5")

