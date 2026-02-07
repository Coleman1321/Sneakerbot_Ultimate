"""
Enhanced Proxy Manager
Handles proxy rotation, testing, and management
"""

import random
import requests
from datetime import datetime
import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import logger, log_proxy_event
from config.settings import PROXY_SETTINGS

class ProxyManager:
    """Manage proxy rotation and testing"""
    
    def __init__(self, proxy_file=None):
        self.proxy_file = proxy_file or PROXY_SETTINGS.get("proxy_list_file", "config/proxies.txt")
        self.proxies = []
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from file"""
        try:
            if os.path.exists(self.proxy_file):
                with open(self.proxy_file, 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                logger.info(f"Loaded {len(self.proxies)} proxies")
            else:
                logger.warning(f"Proxy file not found: {self.proxy_file}")
        except Exception as e:
            logger.error(f"Error loading proxies: {e}")
    
    def get_random_proxy(self):
        """Get a random proxy from the list"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def test_proxy(self, proxy, test_url="https://www.google.com", timeout=10):
        """Test if a proxy is working"""
        try:
            proxies = {
                "http": proxy,
                "https": proxy
            }
            response = requests.get(test_url, proxies=proxies, timeout=timeout)
            success = response.status_code == 200
            log_proxy_event(proxy, success)
            return success
        except Exception:
            log_proxy_event(proxy, False)
            return False
    
    def get_working_proxy(self, max_attempts=5):
        """Get a working proxy by testing them"""
        for _ in range(max_attempts):
            proxy = self.get_random_proxy()
            if proxy and self.test_proxy(proxy):
                return proxy
        return None

# Singleton instance
_proxy_manager = None

def get_proxy_manager():
    """Get proxy manager instance"""
    global _proxy_manager
    if _proxy_manager is None:
        _proxy_manager = ProxyManager()
    return _proxy_manager

def get_random_proxy():
    """Get a random proxy (convenience function)"""
    return get_proxy_manager().get_random_proxy()

def get_working_proxy():
    """Get a working proxy (convenience function)"""
    return get_proxy_manager().get_working_proxy()
