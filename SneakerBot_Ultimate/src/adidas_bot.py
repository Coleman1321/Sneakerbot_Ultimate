from playwright.sync_api import sync_playwright
import time

ADIDAS_HOME_URL = "https://www.adidas.com"

def adidas_login(email, password):
    """Handles Adidas login via pop-up modal with stealth mode."""
    with sync_playwright() as p:
        # ✅ Launch Chromium with stealth-like settings
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context()
        page = context.new_page()

        page.goto(ADIDAS_HOME_URL)
        time.sleep(5)

        # Click on the account icon to open login modal
        account_icon = page.locator("button[data-auto-id='customer-info-button']")
        if account_icon.count() > 0:
            account_icon.click()
            print("✅ Clicked on account icon.")
        else:
            print("❌ Account icon not found!")
            return

        time.sleep(3)  # Wait for modal to appear

        # Fill in email field
        page.fill("input[name='email']", email)

        # Click the Continue button after email input
        continue_button = page.locator("button:has-text('Continue')")
        if continue_button.count() > 0:
            continue_button.click()
            print("✅ Clicked Continue button.")
        else:
            print("❌ Continue button not found!")
            return

        time.sleep(3)  # Wait for password field to appear

        # Fill in password field
        page.fill("input[name='password']", password)

        # Click the Sign In button to log in
        sign_in_button = page.locator("button:has-text('Sign in')")
        if sign_in_button.count() > 0:
            sign_in_button.click()
            print("✅ Clicked Sign In button.")
        else:
            print("❌ Sign In button not found!")
            return

        time.sleep(5)  # Allow time for login to process

        # Verify successful login
        if "account" in page.url:
            print("✅ Successfully logged into Adidas!")
        else:
            print("❌ Login failed!")


def search_sneaker(page, sneaker_name):
    """Search for a specific sneaker and check availability."""
    search_box = page.locator("input[type='search']")
    if search_box.count() > 0:
        search_box.fill(sneaker_name)
        search_box.press("Enter")
        print(f"🔍 Searching for {sneaker_name}...")
        time.sleep(5)
    else:
        print("❌ Search box not found!")
        return None

    # Select first available sneaker
    sneaker = page.locator("a[data-auto-id='product-link']").first
    if sneaker.count() > 0:
        sneaker.click()
        print("✅ Selected sneaker!")
        return True
    else:
        print("❌ Sneaker not found!")
        return False


def add_to_cart(page):
    """Add sneaker to cart and proceed to checkout."""
    add_to_cart_button = page.locator("button:has-text('Add To Bag')")
    if add_to_cart_button.count() > 0:
        add_to_cart_button.click()
        print("✅ Added to cart!")
    else:
        print("❌ Add to cart button not found!")
        return False

    time.sleep(3)
    checkout_button = page.locator("a[href='/cart']")
    if checkout_button.count() > 0:
        checkout_button.click()
        print("🛒 Proceeding to checkout...")
    else:
        print("❌ Checkout button not found!")
        return False
    return True


def enter_adidas_queue(page):
    """Detect and wait in Adidas queue if needed."""
    if "queue" in page.url:
        print("⏳ Entered Adidas queue, waiting...")
        while "queue" in page.url:
            time.sleep(5)
            page.reload()
        print("🚀 Queue finished, proceeding!")
    else:
        print("✅ No queue detected.")


def adidas_checkout(email, password, sneaker_name):
    """Full Adidas sneaker purchase automation."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        page = browser.new_page()
        page.goto(ADIDAS_HOME_URL)
        time.sleep(5)

        adidas_login(email, password)
        time.sleep(5)

        if search_sneaker(page, sneaker_name):
            time.sleep(5)
            enter_adidas_queue(page)
            if add_to_cart(page):
                print("✅ Ready to checkout!")

