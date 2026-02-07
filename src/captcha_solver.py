"""
CAPTCHA Solver Integration
Supports 2Captcha and AntiCaptcha services
"""

import requests
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import API_KEYS, CAPTCHA_CONFIG
from utils.logger import logger

def solve_captcha(site_key, page_url, captcha_type="recaptcha_v2", manual=False):
    """
    Solve CAPTCHA using configured service
    
    Args:
        site_key: Site key for the CAPTCHA
        page_url: URL where CAPTCHA appears
        captcha_type: Type of CAPTCHA (recaptcha_v2, recaptcha_v3, hcaptcha)
        manual: If True, prompt for manual solving
        
    Returns:
        str: CAPTCHA solution token, or None if failed
    """
    
    if manual or not CAPTCHA_CONFIG.get("auto_solve", False):
        logger.info("="*60)
        logger.info("⚠️  MANUAL CAPTCHA SOLVING MODE")
        logger.info("="*60)
        logger.info("A CAPTCHA has appeared in the browser window.")
        logger.info("Please solve it manually, then press Enter here to continue.")
        logger.info("")
        input("👉 Press Enter after you've solved the CAPTCHA...")
        logger.info("✅ Continuing...")
        return "manual"  # Return a marker that manual solving was done
    
    service = CAPTCHA_CONFIG.get("solver_service", "2captcha")
    
    if service == "2captcha":
        return solve_with_2captcha(site_key, page_url, captcha_type)
    elif service == "anticaptcha":
        return solve_with_anticaptcha(site_key, page_url, captcha_type)
    else:
        logger.warning(f"Unknown CAPTCHA service: {service}")
        return None

def solve_with_2captcha(site_key, page_url, captcha_type="recaptcha_v2"):
    """Solve CAPTCHA using 2Captcha service"""
    
    api_key = API_KEYS.get("2Captcha")
    if not api_key or api_key == "YOUR_2CAPTCHA_API_KEY":
        logger.error("2Captcha API key not configured")
        return None
    
    try:
        # Submit CAPTCHA
        logger.info("Submitting CAPTCHA to 2Captcha...")
        
        submit_url = "http://2captcha.com/in.php"
        params = {
            "key": api_key,
            "method": "userrecaptcha",
            "googlekey": site_key,
            "pageurl": page_url,
            "json": 1
        }
        
        response = requests.post(submit_url, data=params)
        result = response.json()
        
        if result.get("status") != 1:
            logger.error(f"2Captcha submission failed: {result.get('request')}")
            return None
        
        captcha_id = result.get("request")
        logger.info(f"CAPTCHA submitted, ID: {captcha_id}")
        
        # Poll for solution
        max_wait = CAPTCHA_CONFIG.get("max_solve_time", 120)
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            time.sleep(5)
            
            result_url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1"
            response = requests.get(result_url)
            result = response.json()
            
            if result.get("status") == 1:
                solution = result.get("request")
                logger.info("✅ CAPTCHA solved successfully")
                return solution
            elif result.get("request") == "CAPCHA_NOT_READY":
                continue
            else:
                logger.error(f"CAPTCHA solving failed: {result.get('request')}")
                return None
        
        logger.error("CAPTCHA solving timed out")
        return None
        
    except Exception as e:
        logger.error(f"Error solving CAPTCHA: {e}")
        return None

def solve_with_anticaptcha(site_key, page_url, captcha_type="recaptcha_v2"):
    """Solve CAPTCHA using AntiCaptcha service"""
    
    api_key = API_KEYS.get("AntiCaptcha")
    if not api_key or api_key == "YOUR_ANTICAPTCHA_API_KEY":
        logger.error("AntiCaptcha API key not configured")
        return None
    
    logger.info("AntiCaptcha integration not yet implemented")
    return None
