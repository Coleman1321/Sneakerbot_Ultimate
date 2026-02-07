"""
Complete Nike/SNKRS Bot Implementation
Security Research Project - Demonstrates bot attack vectors on Nike platform
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import random
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import NIKE_CONFIG, BOT_BEHAVIOR, CAPTCHA_CONFIG
from utils.logger import (
    logger, log_bot_action, log_captcha_event, log_purchase_attempt,
    log_purchase_success, log_purchase_failure, SessionLogger, log_exception
)
from utils.helper_functions import (
    generate_user_agent, generate_browser_fingerprint, random_delay,
    human_typing_delay
)
from src.proxy_manager import get_random_proxy
from src.captcha_solver import solve_captcha


class NikeBot:
    """
    Complete Nike/SNKRS Bot
    
    Features:
    - Stealth mode with fingerprint randomization
    - CAPTCHA solving
    - Proxy rotation
    - Queue handling
    - Size selection automation
    - Checkout automation
    """
    
    def __init__(self, email, password, use_proxy=True):
        self.email = email
        self.password = password
        self.use_proxy = use_proxy
        self.browser = None
        self.context = None
        self.page = None
        self.logged_in = False
        
    def __enter__(self):
        """Context manager entry"""
        self.setup_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
        return False
    
    def setup_browser(self):
        """Initialize browser with stealth settings"""
        log_bot_action("Browser Setup", "Nike", "Initializing with stealth mode")
        
        playwright = sync_playwright().start()
        
        # Launch browser with anti-detection settings
        self.browser = playwright.chromium.launch(
            headless=NIKE_CONFIG["headless"],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-web-security",
            ]
        )
        
        # Generate fingerprint
        fingerprint = generate_browser_fingerprint()
        
        # Create context with proxy if enabled
        context_options = {
            "viewport": {
                "width": fingerprint["screen_resolution"][0],
                "height": fingerprint["screen_resolution"][1]
            },
            "user_agent": generate_user_agent(),
            "locale": "en-US",
            "timezone_id": "America/New_York",
        }
        
        # Add proxy if enabled
        if self.use_proxy:
            proxy = get_random_proxy()
            if proxy:
                context_options["proxy"] = {"server": proxy}
                log_bot_action("Proxy", "Nike", f"Using proxy: {proxy}")
        
        self.context = self.browser.new_context(**context_options)
        
        # Additional stealth measures
        self.context.add_init_script("""
            // Override navigator.webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Override plugins length
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            // Override chrome property
            window.chrome = {
                runtime: {}
            };
            
            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)
        
        self.page = self.context.new_page()
        log_bot_action("Browser Setup", "Nike", "✅ Browser initialized successfully")
    
    def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            log_bot_action("Cleanup", "Nike", "Browser closed")
        except Exception as e:
            log_exception(e, "Browser cleanup")
    
    def login(self):
        """
        Log into Nike account
        
        Returns:
            bool: True if login successful
        """
        with SessionLogger("Nike Login", "Nike"):
            try:
                log_bot_action("Login", "Nike", f"Logging in as {self.email}")
                
                # Navigate to login page
                self.page.goto(NIKE_CONFIG["login_url"], wait_until="networkidle")
                random_delay(2, 4)
                
                # Enter email
                email_field = self.page.locator("input[name='emailAddress']")
                email_field.fill("")  # Clear first
                
                # Type with human-like delay
                for char in self.email:
                    email_field.type(char)
                    time.sleep(random.uniform(0.05, 0.15))
                
                random_delay(0.5, 1.5)
                
                # Enter password
                password_field = self.page.locator("input[name='password']")
                password_field.fill("")  # Clear first
                
                for char in self.password:
                    password_field.type(char)
                    time.sleep(random.uniform(0.05, 0.15))
                
                random_delay(0.5, 1.5)
                
                # Handle CAPTCHA if present
                self._handle_captcha()
                
                # Click sign in button
                sign_in_button = self.page.locator("input[type='submit'][value='SIGN IN']")
                sign_in_button.click()
                
                # Wait for navigation
                random_delay(3, 5)
                
                # Check if login was successful
                if "member" in self.page.url.lower() or "account" in self.page.url.lower():
                    self.logged_in = True
                    log_bot_action("Login", "Nike", "✅ Login successful")
                    return True
                else:
                    log_bot_action("Login", "Nike", "❌ Login failed - checking for errors")
                    return False
                    
            except Exception as e:
                log_exception(e, "Nike Login")
                return False
    
    def _handle_captcha(self):
        """Handle CAPTCHA if present"""
        try:
            # Check for reCAPTCHA
            recaptcha_frame = self.page.locator("iframe[title*='reCAPTCHA']")
            
            if recaptcha_frame.count() > 0:
                log_captcha_event("Nike", "reCAPTCHA", False)
                
                if CAPTCHA_CONFIG["auto_solve"]:
                    # Get site key
                    iframe = recaptcha_frame.first
                    site_key = iframe.get_attribute("data-sitekey")
                    
                    if site_key:
                        log_bot_action("CAPTCHA", "Nike", "Solving CAPTCHA...")
                        solution = solve_captcha(site_key, self.page.url)
                        
                        if solution:
                            # Inject solution
                            self.page.evaluate(f"""
                                document.getElementById('g-recaptcha-response').innerHTML = '{solution}';
                            """)
                            log_captcha_event("Nike", "reCAPTCHA", True)
                        else:
                            log_captcha_event("Nike", "reCAPTCHA", False)
                else:
                    log_bot_action("CAPTCHA", "Nike", "⚠️  Manual CAPTCHA solving required")
                    input("Press Enter after solving CAPTCHA...")
                    
        except Exception as e:
            log_exception(e, "CAPTCHA handling")
    
    def search_sneaker(self, sneaker_name):
        """
        Search for a sneaker
        
        Args:
            sneaker_name: Name of sneaker to search for
            
        Returns:
            str: Product URL if found, None otherwise
        """
        try:
            log_bot_action("Search", "Nike", f"Searching for: {sneaker_name}")
            
            # Click search icon
            search_button = self.page.locator("button[data-pre='HeaderSearchBtn']")
            if search_button.count() > 0:
                search_button.click()
                random_delay(1, 2)
            
            # Type search query
            search_input = self.page.locator("input[type='search']")
            if search_input.count() > 0:
                search_input.fill(sneaker_name)
                search_input.press("Enter")
                random_delay(3, 5)
            
            # Get first product result
            product_link = self.page.locator("a[data-qa='product-card-link']").first
            if product_link.count() > 0:
                product_url = product_link.get_attribute("href")
                log_bot_action("Search", "Nike", f"✅ Found product: {product_url}")
                return product_url
            else:
                log_bot_action("Search", "Nike", "❌ No products found")
                return None
                
        except Exception as e:
            log_exception(e, "Nike Search")
            return None
    
    def select_size(self, size):
        """
        Select shoe size
        
        Args:
            size: Shoe size to select
            
        Returns:
            bool: True if size selected successfully
        """
        try:
            log_bot_action("Size Selection", "Nike", f"Selecting size: {size}")
            
            # Wait for size selector to be visible
            random_delay(1, 2)
            
            # Find size button
            size_str = str(size)
            size_button = self.page.locator(f"button:has-text('US {size_str}')")
            
            if size_button.count() == 0:
                # Try alternate format
                size_button = self.page.locator(f"button[data-qa='size-{size_str}']")
            
            if size_button.count() > 0:
                size_button.first.click()
                random_delay(0.5, 1.5)
                log_bot_action("Size Selection", "Nike", f"✅ Size {size} selected")
                return True
            else:
                log_bot_action("Size Selection", "Nike", f"❌ Size {size} not available")
                return False
                
        except Exception as e:
            log_exception(e, "Size Selection")
            return False
    
    def add_to_cart(self):
        """
        Add item to cart
        
        Returns:
            bool: True if added successfully
        """
        try:
            log_bot_action("Add to Cart", "Nike", "Adding to cart...")
            
            # Click add to cart button
            add_to_cart_btn = self.page.locator("button:has-text('Add to Bag')")
            if add_to_cart_btn.count() == 0:
                add_to_cart_btn = self.page.locator("button[data-qa='add-to-cart']")
            
            if add_to_cart_btn.count() > 0:
                add_to_cart_btn.first.click()
                random_delay(2, 3)
                log_bot_action("Add to Cart", "Nike", "✅ Added to cart")
                return True
            else:
                log_bot_action("Add to Cart", "Nike", "❌ Add to cart button not found")
                return False
                
        except Exception as e:
            log_exception(e, "Add to Cart")
            return False
    
    def go_to_checkout(self):
        """
        Navigate to checkout
        
        Returns:
            bool: True if navigated successfully
        """
        try:
            log_bot_action("Checkout", "Nike", "Navigating to checkout...")
            
            # Click checkout button
            checkout_btn = self.page.locator("button:has-text('Checkout')")
            if checkout_btn.count() == 0:
                checkout_btn = self.page.locator("a[href*='checkout']")
            
            if checkout_btn.count() > 0:
                checkout_btn.first.click()
                random_delay(2, 4)
                log_bot_action("Checkout", "Nike", "✅ Navigated to checkout")
                return True
            else:
                log_bot_action("Checkout", "Nike", "❌ Checkout button not found")
                return False
                
        except Exception as e:
            log_exception(e, "Go to Checkout")
            return False
    
    def enter_snkrs_draw(self, product_url, size):
        """
        Enter SNKRS draw for a product
        
        Args:
            product_url: URL of the product
            size: Shoe size
            
        Returns:
            bool: True if entered successfully
        """
        with SessionLogger("SNKRS Draw Entry", "Nike"):
            try:
                log_purchase_attempt("Nike SNKRS", product_url, size)
                
                # Navigate to product page
                self.page.goto(product_url, wait_until="networkidle")
                random_delay(2, 4)
                
                # Select size
                if not self.select_size(size):
                    return False
                
                # Click "Join Draw" or "Enter Draw" button
                draw_button = self.page.locator("button:has-text('Enter Draw')")
                if draw_button.count() == 0:
                    draw_button = self.page.locator("button:has-text('Join Draw')")
                
                if draw_button.count() > 0:
                    draw_button.first.click()
                    random_delay(2, 3)
                    
                    log_purchase_success("Nike SNKRS", product_url)
                    return True
                else:
                    log_purchase_failure("Nike SNKRS", product_url, "Draw button not found")
                    return False
                    
            except Exception as e:
                log_exception(e, "SNKRS Draw Entry")
                log_purchase_failure("Nike SNKRS", product_url, str(e))
                return False
    
    def complete_purchase(self, sneaker_name, size, product_url=None):
        """
        Complete full purchase flow
        
        Args:
            sneaker_name: Name of sneaker
            size: Shoe size
            product_url: Optional direct product URL
            
        Returns:
            bool: True if purchase successful
        """
        with SessionLogger("Nike Purchase", "Nike"):
            try:
                # Login if not already logged in
                if not self.logged_in:
                    if not self.login():
                        return False
                
                # Navigate to product
                if product_url:
                    self.page.goto(product_url, wait_until="networkidle")
                else:
                    product_url = self.search_sneaker(sneaker_name)
                    if not product_url:
                        return False
                    
                    full_url = f"https://www.nike.com{product_url}" if not product_url.startswith("http") else product_url
                    self.page.goto(full_url, wait_until="networkidle")
                
                random_delay(2, 4)
                
                # Select size
                if not self.select_size(size):
                    return False
                
                # Add to cart
                if not self.add_to_cart():
                    return False
                
                # Go to checkout
                if not self.go_to_checkout():
                    return False
                
                log_purchase_success("Nike", sneaker_name)
                return True
                
            except Exception as e:
                log_exception(e, "Nike Purchase")
                log_purchase_failure("Nike", sneaker_name, str(e))
                return False


# ========================================
# Convenience Functions
# ========================================

def nike_login(email, password, use_proxy=True):
    """
    Login to Nike account
    
    Args:
        email: Nike account email
        password: Nike account password
        use_proxy: Whether to use proxy
        
    Returns:
        NikeBot: Bot instance if successful, None otherwise
    """
    bot = NikeBot(email, password, use_proxy)
    bot.setup_browser()
    
    if bot.login():
        return bot
    else:
        bot.cleanup()
        return None


def nike_purchase(email, password, sneaker_name, size, product_url=None, use_proxy=True):
    """
    Complete Nike purchase
    
    Args:
        email: Nike account email
        password: Nike account password
        sneaker_name: Name of sneaker
        size: Shoe size
        product_url: Optional direct product URL
        use_proxy: Whether to use proxy
        
    Returns:
        bool: True if successful
    """
    with NikeBot(email, password, use_proxy) as bot:
        return bot.complete_purchase(sneaker_name, size, product_url)


def enter_snkrs_draw(email, password, product_url, size, use_proxy=True):
    """
    Enter SNKRS draw
    
    Args:
        email: Nike account email
        password: Nike account password
        product_url: Product URL
        size: Shoe size
        use_proxy: Whether to use proxy
        
    Returns:
        bool: True if successful
    """
    with NikeBot(email, password, use_proxy) as bot:
        if bot.login():
            return bot.enter_snkrs_draw(product_url, size)
        return False


# ========================================
# Testing
# ========================================

if __name__ == "__main__":
    # Demo mode
    print("Nike Bot - Security Research Demo")
    print("=" * 50)
    
    # Test with dummy credentials (will fail, for demo only)
    test_email = "test@example.com"
    test_password = "TestPassword123!"
    
    with NikeBot(test_email, test_password, use_proxy=False) as bot:
        print("Bot initialized successfully")
        print("In production, this would proceed with login and purchase")
