"""
Supreme Bot Implementation
High-speed checkout for Supreme releases
"""
import sys
import os
from playwright.sync_api import sync_playwright

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import logger
from utils.helper_functions import random_delay
from config.settings import SUPREME_CONFIG

class SupremeBot:
    """Supreme-specific bot with speed optimizations"""
    
    def __init__(self):
        self.base_url = SUPREME_CONFIG.get("base_url", "https://www.supremenewyork.com")
        self.browser = None
        self.page = None
    
    def setup_browser(self):
        """Initialize with speed optimizations"""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
    
    def quick_checkout(self, product_url, size, category):
        """Lightning-fast checkout"""
        logger.info(f"Supreme quick checkout: {product_url}")
        
        try:
            self.page.goto(product_url)
            
            # Select size if needed
            if size:
                size_select = self.page.locator("select[name='size']")
                if size_select.count() > 0:
                    size_select.select_option(size)
            
            # Add to cart (immediate click)
            add_btn = self.page.locator("input[name='commit']")
            if add_btn.count() > 0:
                add_btn.click()
            
            random_delay(*SUPREME_CONFIG.get("checkout_delay", (0.5, 1.5)))
            
            # Checkout
            checkout_btn = self.page.locator("a:has-text('checkout')")
            if checkout_btn.count() > 0:
                checkout_btn.click()
            
            logger.info("✅ Supreme checkout initiated")
            return True
            
        except Exception as e:
            logger.exception(f"Supreme checkout error: {e}")
            return False
    
    def cleanup(self):
        if self.browser:
            self.browser.close()

def supreme_checkout(product_url, size=None, category="jackets"):
    """Quick Supreme checkout"""
    bot = SupremeBot()
    bot.setup_browser()
    try:
        return bot.quick_checkout(product_url, size, category)
    finally:
        bot.cleanup()
