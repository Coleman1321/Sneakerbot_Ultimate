"""
Universal Checkout Manager
Handles checkout across multiple platforms
"""
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import logger
from utils.helper_functions import random_delay

class CheckoutManager:
    """Universal checkout handler"""
    
    def __init__(self, platform):
        self.platform = platform
    
    def process_checkout(self, sneaker_id, size, payment_info, shipping_info):
        """Process checkout for any platform"""
        logger.info(f"🛒 Processing checkout: {self.platform}")
        logger.info(f"   Product: {sneaker_id}")
        logger.info(f"   Size: {size}")
        
        # Simulate checkout steps
        steps = [
            "Verifying cart",
            "Processing payment",
            "Confirming shipping",
            "Placing order"
        ]
        
        for step in steps:
            logger.info(f"   {step}...")
            random_delay(1, 3)
        
        logger.info(f"✅ {self.platform} checkout complete!")
        return True

def process_checkout(platform, sneaker_id, size, payment_info=None, shipping_info=None):
    """Quick checkout function"""
    manager = CheckoutManager(platform)
    return manager.process_checkout(sneaker_id, size, payment_info, shipping_info)
