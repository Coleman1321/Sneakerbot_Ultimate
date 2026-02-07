import logging

# ✅ Configure Logging
logging.basicConfig(
    filename="bot.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message):
    """Logs general information"""
    logging.info(message)

def log_error(message):
    """Logs error messages"""
    logging.error(message)

def log_warning(message):
    """Logs warnings"""
    logging.warning(message)

