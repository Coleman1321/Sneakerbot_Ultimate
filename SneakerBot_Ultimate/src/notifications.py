import requests
from config.settings import API_KEYS

DISCORD_WEBHOOK = API_KEYS.get("Discord_Webhook")


def send_discord_notification(message):
    """Sends a Discord notification."""
    if not DISCORD_WEBHOOK:
        print("❌ Discord webhook URL missing!")
        return

    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        if response.status_code == 204:
            print("✅ Discord notification sent!")
        else:
            print(f"❌ Failed to send Discord notification: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Error sending Discord notification: {e}")


# Example Usage
if __name__ == "__main__":
    send_discord_notification("🔥 New sneaker drop detected!")
