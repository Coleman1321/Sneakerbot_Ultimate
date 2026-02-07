# API Documentation

Complete API reference for SneakerBot Ultimate

## Core Bot Classes

### NikeBot

```python
from src.nike_bot import NikeBot

# Initialize
bot = NikeBot(email, password, use_proxy=True)

# Methods
bot.setup_browser()           # Initialize browser
bot.login()                   # Login to account
bot.search_sneaker(name)      # Search for sneaker
bot.select_size(size)         # Select size
bot.add_to_cart()             # Add to cart
bot.go_to_checkout()          # Navigate to checkout
bot.enter_snkrs_draw(url, size)  # Enter SNKRS draw
bot.complete_purchase(name, size)  # Full purchase flow
bot.cleanup()                 # Close browser
```

### AdidasBot

```python
from src.adidas_bot import AdidasBot

bot = AdidasBot(email, password, use_proxy=True)
bot.setup_browser()
bot.login()
bot.handle_queue()           # Handle Adidas queue
bot.search_sneaker(name)
bot.select_size(size)
bot.add_to_cart()
bot.checkout()
bot.complete_purchase(name, size)
```

### ShopifyBot

```python
from src.shopify_bot import ShopifyBot

bot = ShopifyBot(store_url, use_proxy=True)
products = bot.get_products()
stock_info = bot.monitor_stock(keywords, check_interval)
bot.add_to_cart(variant_id, quantity)
checkout_url = bot.get_checkout_url()
```

## Utility Functions

### Proxy Manager

```python
from src.proxy_manager import ProxyManager, get_random_proxy

pm = ProxyManager()
proxy = pm.get_random_proxy()
working_proxy = pm.get_working_proxy()
is_working = pm.test_proxy(proxy)
```

### CAPTCHA Solver

```python
from src.captcha_solver import solve_captcha

solution = solve_captcha(
    site_key="your_site_key",
    page_url="https://example.com",
    captcha_type="recaptcha_v2",
    manual=False
)
```

### Account Manager

```python
from src.account_manager import AccountManager

am = AccountManager()
account_id = am.create_account("Nike", email, password)
account = am.get_account("Nike", account_id)
random_account = am.get_random_account("Nike")
am.update_last_used(account_id)
am.deactivate_account(account_id)
```

## Helper Functions

```python
from utils.helper_functions import (
    generate_random_email,
    generate_user_agent,
    generate_browser_fingerprint,
    random_delay,
    human_typing_delay,
    validate_email,
    normalize_size
)

# Generate test data
email = generate_random_email()
ua = generate_user_agent()
fingerprint = generate_browser_fingerprint()

# Delays
random_delay(2, 5)  # Random 2-5 seconds
delay = human_typing_delay("text to type", wpm=60)

# Validation
is_valid = validate_email("test@example.com")
size = normalize_size("10.5")
```

## Logging

```python
from utils.logger import (
    logger,
    log_bot_action,
    log_purchase_attempt,
    log_purchase_success,
    log_purchase_failure,
    SessionLogger,
    stats
)

# Basic logging
logger.info("Message")
logger.error("Error")

# Bot-specific
log_bot_action("Login", "Nike", "Attempting...")
log_purchase_attempt("Nike", "Jordan 1", "10.5")
log_purchase_success("Nike", "Jordan 1", "ORDER123")

# Session logging
with SessionLogger("Nike Purchase", "Nike"):
    # Your code here
    pass

# Statistics
stats.record_attempt()
stats.record_success()
stats.log_summary()
```

## Notifications

```python
from src.notifications import (
    send_discord_notification,
    send_telegram_notification,
    notify_success,
    notify_failure,
    notify_restock
)

send_discord_notification("Bot completed!")
notify_success("Nike", "Jordan 1", "ORDER123")
notify_restock("Adidas", "Yeezy 350")
```

## Database Operations

```python
import sqlite3

conn = sqlite3.connect("database/userdata.db")
cursor = conn.cursor()

# Query accounts
cursor.execute("SELECT * FROM accounts WHERE platform = ?", ("Nike",))
accounts = cursor.fetchall()

# Insert task
cursor.execute("""
    INSERT INTO tasks (platform, sneaker_name, size, status)
    VALUES (?, ?, ?, ?)
""", ("Nike", "Jordan 1", "10.5", "pending"))

conn.commit()
conn.close()
```

## Configuration

```python
from config.settings import (
    NIKE_CONFIG,
    ADIDAS_CONFIG,
    SHOPIFY_CONFIG,
    BOT_BEHAVIOR,
    CAPTCHA_CONFIG,
    PROXY_SETTINGS
)

# Access settings
headless = NIKE_CONFIG["headless"]
use_proxies = PROXY_SETTINGS["enabled"]
typing_delay = BOT_BEHAVIOR["typing_delay"]
```

## Complete Example

```python
from src.nike_bot import NikeBot
from utils.logger import SessionLogger

with SessionLogger("Nike Bot", "Nike"):
    with NikeBot("user@example.com", "password") as bot:
        if bot.login():
            success = bot.complete_purchase("Air Jordan 1", "10.5")
            if success:
                print("Purchase successful!")
```

See individual module docstrings for more details.
