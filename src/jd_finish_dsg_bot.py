"""
JD Sports, Finish Line, Dick's Sporting Goods Bot
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import logger
from src.checkout_manager import process_checkout

class JDFinishDSGBot:
    """Bot for JD Sports, Finish Line, and DSG"""
    
    SITES = {
        "jd": "https://www.jdsports.com",
        "finishline": "https://www.finishline.com",
        "dsg": "https://www.dickssportinggoods.com",
    }
    
    def __init__(self, site="jd"):
        self.site = site
        self.base_url = self.SITES.get(site)
    
    def checkout(self, sneaker_id, size):
        """Complete checkout"""
        logger.info(f"Starting {self.site.upper()} checkout")
        return process_checkout(self.site, sneaker_id, size)

def jd_finish_dsg_checkout(site, sneaker_id, size):
    """Convenience function"""
    bot = JDFinishDSGBot(site)
    return bot.checkout(sneaker_id, size)
