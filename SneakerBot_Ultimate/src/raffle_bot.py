import requests
import random
import time
from utils.helper_functions import generate_random_email
from src.proxy_manager import get_random_proxy


def enter_raffle(site, sneaker_id, size, email=None, proxy=None):
    """Submits a raffle entry on a given sneaker site."""

    proxies = {"http": proxy, "https": proxy} if proxy else None

    if not email:
        email = generate_random_email()

    payload = {
        "sneaker_id": sneaker_id,
        "size": size,
        "email": email,
        "accept_terms": "true"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"https://{site}/raffle/enter", json=payload, headers=headers, proxies=proxies)
        if response.status_code == 200:
            print(f"✅ Successfully entered raffle on {site} for sneaker {sneaker_id} in size {size}.")
        else:
            print(f"❌ Failed to enter raffle on {site}: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"❌ Error entering raffle on {site}: {e}")


# Example usage
if __name__ == "__main__":
    enter_raffle("sns.com", "nike-travis-scott", "10.5", proxy=get_random_proxy())

