"""
Complete Adidas Bot Implementation
Handles login, queue, search, and checkout for Adidas platform
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import ADIDAS_CONFIG, BOT_BEHAVIOR
from utils.logger import logger, log_bot_action, log_purchase_attempt, log_purchase_success, log_purchase_failure, SessionLogger
from utils.helper_functions import generate_user_agent, random_delay
from src.proxy_manager import get_random_proxy

ADIDAS_HOME_URL = "https://www.adidas.com"

class AdidasBot:
    """Complete Adidas bot with queue handling and stealth"""
    
    def __init__(self, email, password, use_proxy=True):
        self.email = email
        self.password = password
        self.use_proxy = use_proxy
        self.browser = None
        self.page = None
        self.logged_in = False
    
    def setup_browser(self):
        """Initialize browser with stealth"""
        log_bot_action("Browser Setup", "Adidas", "Initializing")
        
        playwright = sync_playwright().start()
        
        launch_args = ["--disable-blink-features=AutomationControlled"]
        if ADIDAS_CONFIG.get("stealth_mode"):
            launch_args.extend(["--disable-dev-shm-usage", "--no-sandbox"])
        
        self.browser = playwright.chromium.launch(
            headless=ADIDAS_CONFIG.get("headless", False),
            args=launch_args
        )
        
        context_options = {"user_agent": generate_user_agent()}
        
        if self.use_proxy:
            proxy = get_random_proxy()
            if proxy:
                context_options["proxy"] = {"server": proxy}
        
        context = self.browser.new_context(**context_options)
        self.page = context.new_page()
        
        log_bot_action("Browser Setup", "Adidas", "✅ Initialized")
    
    def login(self):
        """Login to Adidas account"""
        with SessionLogger("Adidas Login", "Adidas"):
            try:
                self.page.goto(ADIDAS_HOME_URL)
                random_delay(2, 4)
                
                # Click account icon
                account_btn = self.page.locator("button[data-auto-id='customer-info-button']")
                if account_btn.count() > 0:
                    account_btn.click()
                    random_delay(1, 2)
                
                # Enter email
                self.page.fill("input[name='email']", self.email)
                random_delay(0.5, 1)
                
                # Click continue
                continue_btn = self.page.locator("button:has-text('Continue')")
                if continue_btn.count() > 0:
                    continue_btn.click()
                    random_delay(2, 3)
                
                # Enter password
                self.page.fill("input[name='password']", self.password)
                random_delay(0.5, 1)
                
                # Sign in
                sign_in_btn = self.page.locator("button:has-text('Sign in')")
                if sign_in_btn.count() > 0:
                    sign_in_btn.click()
                    random_delay(3, 5)
                
                self.logged_in = "account" in self.page.url
                log_bot_action("Login", "Adidas", "✅ Success" if self.logged_in else "❌ Failed")
                return self.logged_in
                
            except Exception as e:
                logger.exception(f"Adidas login error: {e}")
                return False
    
    def handle_queue(self):
        """Handle Adidas waiting queue"""
        if "queue" not in self.page.url:
            return True
        
        log_bot_action("Queue", "Adidas", "Detected - waiting")
        max_wait = ADIDAS_CONFIG.get("max_queue_wait", 3600)
        start_time = time.time()
        
        while "queue" in self.page.url and (time.time() - start_time) < max_wait:
            random_delay(ADIDAS_CONFIG.get("queue_refresh_interval", 5), 7)
            self.page.reload()
        
        if "queue" not in self.page.url:
            log_bot_action("Queue", "Adidas", "✅ Passed")
            return True
        else:
            log_bot_action("Queue", "Adidas", "❌ Timeout")
            return False
    
    def search_sneaker(self, sneaker_name):
        """Search for sneaker"""
        try:
            search_box = self.page.locator("input[type='search']")
            if search_box.count() > 0:
                search_box.fill(sneaker_name)
                search_box.press("Enter")
                random_delay(3, 5)
                
                # Click first result
                product = self.page.locator("a[data-auto-id='product-link']").first
                if product.count() > 0:
                    product.click()
                    random_delay(2, 4)
                    return True
            
            return False
        except Exception as e:
            logger.exception(f"Adidas search error: {e}")
            return False
    
    def select_size(self, size):
        """Select shoe size"""
        try:
            size_button = self.page.locator(f"button:has-text('{size}')")
            if size_button.count() > 0:
                size_button.first.click()
                random_delay(1, 2)
                return True
            return False
        except Exception as e:
            logger.exception(f"Size selection error: {e}")
            return False
    
    def add_to_cart(self):
        """Add to cart"""
        try:
            add_btn = self.page.locator("button:has-text('Add To Bag')")
            if add_btn.count() > 0:
                add_btn.click()
                random_delay(2, 3)
                return True
            return False
        except Exception as e:
            logger.exception(f"Add to cart error: {e}")
            return False
    
    def checkout(self):
        """Go to checkout"""
        try:
            checkout_btn = self.page.locator("a[href*='checkout']")
            if checkout_btn.count() > 0:
                checkout_btn.click()
                random_delay(2, 4)
                return True
            return False
        except Exception as e:
            logger.exception(f"Checkout error: {e}")
            return False
    
    def complete_purchase(self, sneaker_name, size):
        """Complete full purchase flow"""
        with SessionLogger("Adidas Purchase", "Adidas"):
            try:
                if not self.logged_in and not self.login():
                    return False
                
                if not self.search_sneaker(sneaker_name):
                    return False
                
                if not self.handle_queue():
                    return False
                
                if not self.select_size(size):
                    return False
                
                if not self.add_to_cart():
                    return False
                
                if not self.checkout():
                    return False
                
                log_purchase_success("Adidas", sneaker_name)
                return True
                
            except Exception as e:
                log_purchase_failure("Adidas", sneaker_name, str(e))
                return False
    
    def cleanup(self):
        """Close browser"""
        if self.browser:
            self.browser.close()


def adidas_checkout(email, password, sneaker_name, size="10", use_proxy=True):
    """Convenience function for Adidas checkout"""
    bot = AdidasBot(email, password, use_proxy)
    bot.setup_browser()
    try:
        return bot.complete_purchase(sneaker_name, size)
    finally:
        bot.cleanup()
