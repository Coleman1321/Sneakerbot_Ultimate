import requests
import time
from config.settings import API_KEYS


def solve_captcha(site_key, page_url, manual=False):
    """Solves CAPTCHA either automatically or manually."""
    if manual:
        return input("Enter CAPTCHA manually: ")

    API_KEY = API_KEYS.get("2Captcha")
    response = requests.post("http://2captcha.com/in.php", data={
        "key": API_KEY,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": page_url,
        "json": 1
    }).json()

    if response["status"] != 1:
        return None

    request_id = response["request"]
    time.sleep(15)

    for _ in range(10):
        result = requests.get(f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={request_id}&json=1").json()
        if result["status"] == 1:
            return result["request"]
        time.sleep(5)

    return None