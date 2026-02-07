"""
Footsites Bot - FootLocker, Champs, Eastbay
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright
from utils.logger import logger, log_bot_action
from utils.helper_functions import random_delay
import time

class FootsitesBot:
    """Bot for Footsites (FootLocker, Champs, Eastbay)"""
    
    SITES = {
        "footlocker": "https://www.footlocker.com",
        "champs": "https://www.champssports.com",
        "eastbay": "https://www.eastbay.com",
    }
    
    def __init__(self, site="footlocker"):
        self.base_url = self.SITES.get(site, self.SITES["footlocker"])
        self.site_name = site
        self.browser = None
        self.page = None
    
    def setup_browser(self):
        """Initialize browser"""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
    
    def search_product(self, product_name):
        """Search for product"""
        try:
            self.page.goto(self.base_url)
            random_delay(2, 4)
            
            search_box = self.page.locator("input[type='search']")
            if search_box.count() > 0:
                search_box.fill(product_name)
                search_box.press("Enter")
                random_delay(3, 5)
                return True
            return False
        except Exception as e:
            logger.exception(f"Footsites search error: {e}")
            return False
    
    def select_size(self, size):
        """Select size"""
        try:
            size_btn = self.page.locator(f"button:has-text('{size}')")
            if size_btn.count() > 0:
                size_btn.first.click()
                random_delay(1, 2)
                return True
            return False
        except Exception as e:
            logger.exception(f"Size select error: {e}")
            return False
    
    def add_to_cart(self):
        """Add to cart"""
        try:
            add_btn = self.page.locator("button:has-text('Add to Cart')")
            if add_btn.count() > 0:
                add_btn.click()
                random_delay(2, 3)
                return True
            return False
        except Exception as e:
            logger.exception(f"Add to cart error: {e}")
            return False
    
    def cleanup(self):
        if self.browser:
            self.browser.close()

def footsites_checkout(site, product_name, size):
    """Footsites checkout"""
    bot = FootsitesBot(site)
    bot.setup_browser()
    try:
        if bot.search_product(product_name):
            if bot.select_size(size):
                return bot.add_to_cart()
        return False
    finally:
        bot.cleanup()
