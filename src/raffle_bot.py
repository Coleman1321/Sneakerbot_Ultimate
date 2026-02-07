"""
Raffle Entry Bot
Automates raffle entries across platforms
"""
import requests
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helper_functions import generate_random_email, generate_random_name, generate_random_phone, generate_random_address
from utils.logger import logger
from src.proxy_manager import get_random_proxy

class RaffleBot:
    """Automated raffle entry system"""
    
    def __init__(self, use_proxies=True):
        self.use_proxies = use_proxies
        self.entries = []
    
    def enter_raffle(self, site_url, sneaker_id, size, num_entries=1):
        """Enter raffle multiple times"""
        logger.info(f"Entering raffle: {site_url} - {sneaker_id} (Size: {size})")
        
        for i in range(num_entries):
            email = generate_random_email()
            name = generate_random_name()
            phone = generate_random_phone()
            address = generate_random_address()
            
            entry_data = {
                "email": email,
                "first_name": name["first_name"],
                "last_name": name["last_name"],
                "phone": phone,
                "sneaker_id": sneaker_id,
                "size": size,
                **address
            }
            
            # Simulate raffle entry
            success = self._submit_entry(site_url, entry_data)
            
            if success:
                self.entries.append(entry_data)
                logger.info(f"✅ Entry {i+1}/{num_entries} submitted: {email}")
            else:
                logger.error(f"❌ Entry {i+1}/{num_entries} failed")
            
            time.sleep(2)  # Delay between entries
        
        logger.info(f"Completed {len(self.entries)} raffle entries")
        return len(self.entries)
    
    def _submit_entry(self, site_url, entry_data):
        """Submit a single raffle entry"""
        try:
            proxies = None
            if self.use_proxies:
                proxy = get_random_proxy()
                if proxy:
                    proxies = {"http": proxy, "https": proxy}
            
            # This is a simulation - actual implementation would POST to raffle endpoint
            # response = requests.post(f"{site_url}/api/raffle", json=entry_data, proxies=proxies)
            # return response.status_code == 200
            
            return True  # Simulated success
            
        except Exception as e:
            logger.exception(f"Raffle entry error: {e}")
            return False

def enter_raffle(site_url, sneaker_id, size, num_entries=1):
    """Convenience function for raffle entry"""
    bot = RaffleBot()
    return bot.enter_raffle(site_url, sneaker_id, size, num_entries)
