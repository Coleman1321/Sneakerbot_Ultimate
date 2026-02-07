"""
Complete Shopify Bot Implementation
Universal bot for Shopify-based stores
"""

import requests
import json
import time
import sys
import os
from urllib.parse import urljoin

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import SHOPIFY_CONFIG
from utils.logger import logger, log_bot_action, log_stock_alert
from src.proxy_manager import get_random_proxy
from utils.helper_functions import random_delay

class ShopifyBot:
    """Universal Shopify store bot"""
    
    def __init__(self, store_url, use_proxy=True):
        self.store_url = store_url.rstrip('/')
        self.use_proxy = use_proxy
        self.session = requests.Session()
        
        if use_proxy:
            proxy = get_random_proxy()
            if proxy:
                self.session.proxies = {"http": proxy, "https": proxy}
    
    def get_products(self):
        """Get all products via products.json"""
        try:
            url = f"{self.store_url}/products.json"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("products", [])
            else:
                logger.error(f"Failed to get products: {response.status_code}")
                return []
                
        except Exception as e:
            logger.exception(f"Error getting products: {e}")
            return []
    
    def monitor_stock(self, keywords, check_interval=None):
        """Monitor for stock with keywords"""
        interval = check_interval or SHOPIFY_CONFIG.get("monitor_interval", 2)
        
        log_bot_action("Stock Monitor", "Shopify", f"Monitoring {self.store_url}")
        
        while True:
            try:
                products = self.get_products()
                
                for product in products:
                    title = product.get("title", "").lower()
                    
                    # Check if any keyword matches
                    if any(keyword.lower() in title for keyword in keywords):
                        # Check if in stock
                        variants = product.get("variants", [])
                        for variant in variants:
                            if variant.get("available"):
                                log_stock_alert("Shopify", product["title"])
                                return {
                                    "product_id": product["id"],
                                    "variant_id": variant["id"],
                                    "title": product["title"],
                                    "price": variant.get("price"),
                                }
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Stock monitoring stopped")
                break
            except Exception as e:
                logger.exception(f"Stock monitor error: {e}")
                time.sleep(interval)
        
        return None
    
    def add_to_cart(self, variant_id, quantity=1):
        """Add item to cart via cart API"""
        try:
            url = f"{self.store_url}/cart/add.js"
            data = {"id": variant_id, "quantity": quantity}
            
            response = self.session.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                log_bot_action("Add to Cart", "Shopify", "✅ Success")
                return True
            else:
                log_bot_action("Add to Cart", "Shopify", f"❌ Failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.exception(f"Add to cart error: {e}")
            return False
    
    def get_checkout_url(self):
        """Get checkout URL"""
        return f"{self.store_url}/checkout"
    
    def quick_checkout(self, variant_id, size=None):
        """Quick add and go to checkout"""
        if self.add_to_cart(variant_id):
            checkout_url = self.get_checkout_url()
            log_bot_action("Checkout", "Shopify", f"Go to: {checkout_url}")
            return checkout_url
        return None


def monitor_shopify_stock(store_url, keywords):
    """Monitor Shopify store for keywords"""
    bot = ShopifyBot(store_url)
    return bot.monitor_stock(keywords)

def checkout_shopify(store_url, variant_id, size=None):
    """Quick checkout on Shopify"""
    bot = ShopifyBot(store_url)
    return bot.quick_checkout(variant_id, size)
