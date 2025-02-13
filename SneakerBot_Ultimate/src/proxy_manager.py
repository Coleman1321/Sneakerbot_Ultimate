import random

def load_proxies(proxy_file="config/proxies.txt"):
    """Loads proxy list from file"""
    try:
        with open(proxy_file, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies if proxies else None
    except FileNotFoundError:
        return None

def get_random_proxy():
    """Returns a random proxy from the list"""
    proxies = load_proxies()
    if proxies:
        return random.choice(proxies)
    return None

