"""
Notification System
Discord and Telegram notifications
"""
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import API_KEYS, NOTIFICATION_CONFIG
from utils.logger import logger

def send_discord_notification(message):
    """Send Discord webhook notification"""
    if not NOTIFICATION_CONFIG.get("discord_enabled"):
        return False
    
    webhook_url = API_KEYS.get("Discord_Webhook")
    if not webhook_url or webhook_url == "YOUR_DISCORD_WEBHOOK_URL":
        logger.warning("Discord webhook not configured")
        return False
    
    try:
        payload = {"content": message}
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 204:
            logger.info("✅ Discord notification sent")
            return True
        else:
            logger.error(f"Discord notification failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.exception(f"Discord notification error: {e}")
        return False

def send_telegram_notification(message):
    """Send Telegram notification"""
    if not NOTIFICATION_CONFIG.get("telegram_enabled"):
        return False
    
    bot_token = API_KEYS.get("Telegram_Bot_Token")
    chat_id = API_KEYS.get("Telegram_Chat_ID")
    
    if not bot_token or not chat_id:
        logger.warning("Telegram not configured")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ Telegram notification sent")
            return True
        else:
            logger.error(f"Telegram notification failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.exception(f"Telegram notification error: {e}")
        return False

def notify_success(platform, sneaker_name, order_number=None):
    """Send success notification"""
    message = f"🎉 SUCCESS: Purchased {sneaker_name} on {platform}"
    if order_number:
        message += f"\nOrder: {order_number}"
    
    send_discord_notification(message)
    send_telegram_notification(message)

def notify_failure(platform, sneaker_name, reason=None):
    """Send failure notification"""
    message = f"❌ FAILED: {sneaker_name} on {platform}"
    if reason:
        message += f"\nReason: {reason}"
    
    send_discord_notification(message)

def notify_restock(platform, sneaker_name):
    """Send restock notification"""
    message = f"🔥 RESTOCK ALERT: {sneaker_name} on {platform}"
    send_discord_notification(message)
    send_telegram_notification(message)
