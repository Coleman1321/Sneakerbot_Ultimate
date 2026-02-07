"""
SneakerBot Ultimate - Configuration File
Security Research Project

This configuration demonstrates various attack vectors and bot capabilities
for educational and security research purposes only.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ========================================
# API Keys & External Services
# ========================================
API_KEYS = {
    # CAPTCHA Solving Services
    "2Captcha": os.getenv("CAPTCHA_API_KEY", "YOUR_2CAPTCHA_API_KEY"),
    "AntiCaptcha": os.getenv("ANTICAPTCHA_API_KEY", "YOUR_ANTICAPTCHA_API_KEY"),
    
    # Notification Services
    "Discord_Webhook": os.getenv("DISCORD_WEBHOOK", "YOUR_DISCORD_WEBHOOK_URL"),
    "Telegram_Bot_Token": os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN"),
    "Telegram_Chat_ID": os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID"),
    
    # AI Services (for auto-fix feature)
    "OpenAI": os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"),
    "Anthropic": os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY"),
}

# ========================================
# Proxy Configuration
# ========================================
PROXY_SETTINGS = {
    "enabled": True,
    "proxy_list_file": "config/proxies.txt",
    "rotate_on_failure": True,
    "max_retries_per_proxy": 3,
    "test_proxies_on_start": True,
    "timeout": 30,  # seconds
}

# ========================================
# Database Configuration
# ========================================
DATABASE_CONFIG = {
    "main_db": "database/userdata.db",
    "backup_enabled": True,
    "backup_interval": 3600,  # seconds (1 hour)
    "backup_path": "backup/",
}

# ========================================
# Platform-Specific Settings
# ========================================

# Nike/SNKRS Configuration
NIKE_CONFIG = {
    "base_url": "https://www.nike.com",
    "login_url": "https://www.nike.com/login",
    "snkrs_url": "https://www.nike.com/launch",
    "checkout_delay": (2, 5),  # Random delay range in seconds
    "max_retries": 3,
    "headless": False,
    "stealth_mode": True,
}

# Adidas Configuration
ADIDAS_CONFIG = {
    "base_url": "https://www.adidas.com",
    "login_url": "https://www.adidas.com/us/account-login",
    "queue_refresh_interval": 5,  # seconds
    "max_queue_wait": 3600,  # 1 hour max wait in queue
    "headless": False,
    "stealth_mode": True,
    "bypass_queue_attempt": False,  # For research purposes only
}

# Shopify Configuration
SHOPIFY_CONFIG = {
    "monitor_interval": 2,  # seconds between stock checks
    "checkout_delay": (1, 3),
    "use_product_json": True,
    "use_cart_api": True,
    "max_retries": 5,
}

# Footsites Configuration (FootLocker, Champs, Eastbay)
FOOTSITES_CONFIG = {
    "sites": {
        "footlocker": "https://www.footlocker.com",
        "champs": "https://www.champssports.com",
        "eastbay": "https://www.eastbay.com",
    },
    "session_token_refresh": True,
    "headless": False,
}

# Supreme Configuration
SUPREME_CONFIG = {
    "base_url": "https://www.supremenewyork.com",
    "checkout_delay": (0.5, 1.5),  # Very fast checkout
    "autofill_speed": "fast",  # 'slow', 'medium', 'fast'
}

# ========================================
# Bot Behavior Settings
# ========================================
BOT_BEHAVIOR = {
    # Human-like delays
    "typing_delay": (0.05, 0.15),  # seconds per character
    "click_delay": (0.1, 0.3),  # seconds before clicking
    "page_load_wait": (2, 4),  # seconds to wait for page load
    
    # Mouse movement
    "human_mouse_movement": True,
    "mouse_speed": "medium",  # 'slow', 'medium', 'fast'
    
    # Browser fingerprinting
    "randomize_user_agent": True,
    "randomize_screen_size": True,
    "randomize_fonts": True,
    "disable_webrtc": True,
    "disable_webgl": False,
    
    # Session management
    "clear_cookies_between_runs": False,
    "use_persistent_session": True,
    "session_timeout": 1800,  # 30 minutes
}

# ========================================
# CAPTCHA Settings
# ========================================
CAPTCHA_CONFIG = {
    "auto_solve": True,
    "solver_service": "2captcha",  # '2captcha', 'anticaptcha', 'manual'
    "max_solve_time": 120,  # seconds
    "retry_on_failure": True,
    "captcha_sound": False,
}

# ========================================
# Monitoring & Stock Alerts
# ========================================
MONITORING_CONFIG = {
    "enabled": True,
    "check_interval": 5,  # seconds
    "platforms": ["Nike", "Adidas", "Shopify", "Supreme"],
    "keywords": ["Jordan", "Yeezy", "Dunk", "Travis Scott"],
    "notify_on_restock": True,
    "auto_checkout_on_restock": False,  # Set to True for full automation
}

# ========================================
# Notification Settings
# ========================================
NOTIFICATION_CONFIG = {
    "discord_enabled": True,
    "telegram_enabled": False,
    "email_enabled": False,
    
    # What to notify about
    "notify_on_success": True,
    "notify_on_failure": True,
    "notify_on_restock": True,
    "notify_on_captcha": False,
    "notify_on_queue": True,
    
    # Rate limiting for notifications
    "max_notifications_per_minute": 5,
}

# ========================================
# Multi-Threading & Performance
# ========================================
PERFORMANCE_CONFIG = {
    "multi_threading": True,
    "max_workers": 5,  # Number of concurrent tasks
    "max_accounts_per_release": 3,
    "task_queue_size": 10,
    "memory_limit_mb": 2048,
}

# ========================================
# Retry & Error Handling
# ========================================
ERROR_HANDLING = {
    "max_retries": 3,
    "retry_delay": (5, 10),  # seconds
    "exponential_backoff": True,
    "backoff_factor": 2,
    "retry_on_rate_limit": True,
    "rate_limit_wait": 60,  # seconds
}

# ========================================
# Logging Configuration
# ========================================
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "log_to_file": True,
    "log_file": "bot.log",
    "log_to_console": True,
    "max_log_size_mb": 10,
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "colorize": True,
}

# ========================================
# Security Research Features
# ========================================
RESEARCH_CONFIG = {
    # Attack vector demonstration
    "demonstrate_rate_limiting": True,
    "demonstrate_queue_bypass": True,
    "demonstrate_captcha_solving": True,
    "demonstrate_fingerprint_randomization": True,
    "demonstrate_proxy_rotation": True,
    
    # Metrics collection for defense analysis
    "collect_performance_metrics": True,
    "collect_failure_patterns": True,
    "collect_detection_events": True,
    
    # Generate security report
    "generate_security_report": True,
    "report_output_path": "docs/security_analysis_report.md",
}

# ========================================
# Advanced Features (Optional)
# ========================================
ADVANCED_FEATURES = {
    # AI-powered auto-fix
    "ai_auto_fix": False,  # Requires OpenAI/Anthropic API key
    "auto_fix_model": "gpt-4",  # or "claude-3-opus"
    
    # Machine learning for pattern recognition
    "ml_success_prediction": False,
    
    # Blockchain/NFT integration
    "nft_monitoring": False,
    
    # Advanced analytics
    "analytics_dashboard": False,
}

# ========================================
# Safety & Ethics
# ========================================
SAFETY_CONFIG = {
    # Automatic safety limits
    "max_purchase_attempts": 10,  # Per release
    "require_manual_confirmation": False,
    "dry_run_mode": False,  # Test without actual purchases
    
    # Compliance
    "respect_robots_txt": True,
    "rate_limit_compliance": True,
    "terms_of_service_acknowledged": True,
}

# ========================================
# File Paths
# ========================================
PATHS = {
    "screenshots": "screenshots/",
    "logs": "logs/",
    "backup": "backup/",
    "temp": "temp/",
    "exports": "exports/",
}

# ========================================
# Development Settings
# ========================================
DEV_CONFIG = {
    "debug_mode": False,
    "verbose_logging": False,
    "save_screenshots": True,
    "save_html_snapshots": False,
    "test_mode": False,
}


# ========================================
# Helper Functions
# ========================================

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Check for required API keys if features are enabled
    if CAPTCHA_CONFIG["auto_solve"] and API_KEYS["2Captcha"] == "YOUR_2CAPTCHA_API_KEY":
        errors.append("⚠️  CAPTCHA auto-solve enabled but no API key configured")
    
    if NOTIFICATION_CONFIG["discord_enabled"] and API_KEYS["Discord_Webhook"] == "YOUR_DISCORD_WEBHOOK_URL":
        errors.append("⚠️  Discord notifications enabled but no webhook configured")
    
    # Check for required files
    if PROXY_SETTINGS["enabled"]:
        if not os.path.exists(PROXY_SETTINGS["proxy_list_file"]):
            errors.append(f"⚠️  Proxy file not found: {PROXY_SETTINGS['proxy_list_file']}")
    
    return errors


def print_config_status():
    """Print current configuration status"""
    print("=" * 50)
    print("SneakerBot Ultimate - Configuration Status")
    print("=" * 50)
    print(f"Proxy Rotation: {'✅ Enabled' if PROXY_SETTINGS['enabled'] else '❌ Disabled'}")
    print(f"CAPTCHA Solving: {'✅ Enabled' if CAPTCHA_CONFIG['auto_solve'] else '❌ Disabled'}")
    print(f"Discord Notifications: {'✅ Enabled' if NOTIFICATION_CONFIG['discord_enabled'] else '❌ Disabled'}")
    print(f"Multi-Threading: {'✅ Enabled' if PERFORMANCE_CONFIG['multi_threading'] else '❌ Disabled'}")
    print(f"Stock Monitoring: {'✅ Enabled' if MONITORING_CONFIG['enabled'] else '❌ Disabled'}")
    print(f"Debug Mode: {'✅ Enabled' if DEV_CONFIG['debug_mode'] else '❌ Disabled'}")
    print("=" * 50)
    
    # Show validation errors
    errors = validate_config()
    if errors:
        print("\n⚠️  Configuration Warnings:")
        for error in errors:
            print(f"   {error}")
    else:
        print("\n✅ Configuration validated successfully!")
    print("=" * 50)


if __name__ == "__main__":
    print_config_status()
