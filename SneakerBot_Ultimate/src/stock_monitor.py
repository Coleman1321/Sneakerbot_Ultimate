import requests
import time

STOCK_API_URL = "https://api.sneakerstock.com/check/{sneaker_id}"

def check_stock(sneaker_id):
    """Checks stock availability for a given sneaker."""
    try:
        response = requests.get(STOCK_API_URL.format(sneaker_id=sneaker_id))
        if response.status_code == 200:
            data = response.json()
            if data["in_stock"]:
                print(f"🔥 Sneaker {sneaker_id} is IN STOCK!")
                return True
            else:
                print(f"❌ Sneaker {sneaker_id} is OUT OF STOCK.")
        else:
            print(f"❌ Failed to check stock for {sneaker_id}: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Error checking stock: {e}")
    return False

# Example Usage
if __name__ == "__main__":
    check_stock("nike-travis-scott")

