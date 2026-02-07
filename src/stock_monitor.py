"""
Stock Monitoring System
Monitors multiple platforms for restocks
"""
import requests
import time
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import logger, log_stock_alert
from src.notifications import send_discord_notification
from config.settings import MONITORING_CONFIG

class StockMonitor:
    """Multi-platform stock monitor"""
    
    def __init__(self):
        self.monitoring = []
        self.check_interval = MONITORING_CONFIG.get("check_interval", 5)
    
    def add_monitor(self, platform, product_url, keywords=None):
        """Add a product to monitor"""
        self.monitoring.append({
            "platform": platform,
            "url": product_url,
            "keywords": keywords or [],
            "last_check": None,
            "in_stock": False
        })
        logger.info(f"Added monitor: {platform} - {product_url}")
    
    def check_stock_generic(self, url):
        """Generic stock check via HTTP"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Simple check - look for common out of stock indicators
                content = response.text.lower()
                out_of_stock_indicators = [
                    "out of stock",
                    "sold out",
                    "unavailable",
                    "not available"
                ]
                
                for indicator in out_of_stock_indicators:
                    if indicator in content:
                        return False
                
                return True  # Likely in stock
            return False
        except Exception as e:
            logger.error(f"Stock check error for {url}: {e}")
            return False
    
    def start_monitoring(self):
        """Start monitoring loop"""
        logger.info(f"Starting stock monitor ({len(self.monitoring)} products)")
        
        try:
            while True:
                for item in self.monitoring:
                    current_stock = self.check_stock_generic(item["url"])
                    
                    # If newly in stock, notify
                    if current_stock and not item["in_stock"]:
                        log_stock_alert(item["platform"], item["url"])
                        
                        if MONITORING_CONFIG.get("notify_on_restock"):
                            message = f"🔥 RESTOCK: {item['platform']}\n{item['url']}"
                            send_discord_notification(message)
                    
                    item["in_stock"] = current_stock
                    item["last_check"] = datetime.now()
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("Stock monitoring stopped by user")
        except Exception as e:
            logger.exception(f"Stock monitor error: {e}")

def check_stock(product_url):
    """Quick stock check"""
    monitor = StockMonitor()
    return monitor.check_stock_generic(product_url)
