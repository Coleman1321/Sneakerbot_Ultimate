"""
Enhanced Logging System for SneakerBot Ultimate
Provides colored console output and file logging with rotation
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os

# Color codes for terminal output
class LogColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support"""
    
    COLORS = {
        'DEBUG': LogColors.OKBLUE,
        'INFO': LogColors.OKGREEN,
        'WARNING': LogColors.WARNING,
        'ERROR': LogColors.FAIL,
        'CRITICAL': LogColors.FAIL + LogColors.BOLD,
    }
    
    def format(self, record):
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{LogColors.ENDC}"
        
        return super().format(record)


def setup_logger(name="SneakerBot", level=logging.INFO, log_file="bot.log"):
    """
    Set up logger with both file and console handlers
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_format = ColoredFormatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # File handler with rotation (10MB max, keep 5 backups)
    os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else ".", exist_ok=True)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)  # Capture everything in file
    file_handler.setFormatter(file_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_format)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Create default logger instance
logger = setup_logger()


# ========================================
# Convenience Functions
# ========================================

def log_info(message, *args, **kwargs):
    """Log informational message"""
    logger.info(message, *args, **kwargs)


def log_debug(message, *args, **kwargs):
    """Log debug message"""
    logger.debug(message, *args, **kwargs)


def log_warning(message, *args, **kwargs):
    """Log warning message"""
    logger.warning(message, *args, **kwargs)


def log_error(message, *args, **kwargs):
    """Log error message"""
    logger.error(message, *args, **kwargs)


def log_critical(message, *args, **kwargs):
    """Log critical message"""
    logger.critical(message, *args, **kwargs)


def log_success(message):
    """Log success message with special formatting"""
    logger.info(f"✅ {message}")


def log_failure(message):
    """Log failure message with special formatting"""
    logger.error(f"❌ {message}")


def log_progress(current, total, prefix="Progress"):
    """Log progress message"""
    percentage = (current / total) * 100 if total > 0 else 0
    logger.info(f"{prefix}: {current}/{total} ({percentage:.1f}%)")


def log_task_start(task_name):
    """Log task start"""
    logger.info(f"🚀 Starting task: {task_name}")


def log_task_end(task_name, success=True):
    """Log task completion"""
    if success:
        logger.info(f"✅ Task completed: {task_name}")
    else:
        logger.error(f"❌ Task failed: {task_name}")


def log_separator():
    """Log visual separator"""
    logger.info("=" * 60)


def log_section(section_name):
    """Log section header"""
    log_separator()
    logger.info(f"  {section_name.upper()}")
    log_separator()


# ========================================
# Task-Specific Logging
# ========================================

def log_bot_action(action, platform, details=None):
    """
    Log bot action with context
    
    Args:
        action: Action being performed (login, checkout, etc.)
        platform: Platform name (Nike, Adidas, etc.)
        details: Optional additional details
    """
    message = f"[{platform}] {action}"
    if details:
        message += f" - {details}"
    logger.info(message)


def log_captcha_event(platform, captcha_type, success):
    """Log CAPTCHA solving event"""
    status = "✅ Solved" if success else "❌ Failed"
    logger.info(f"[{platform}] CAPTCHA ({captcha_type}): {status}")


def log_proxy_event(proxy, success):
    """Log proxy usage"""
    status = "✅ Working" if success else "❌ Failed"
    logger.debug(f"Proxy {proxy}: {status}")


def log_queue_event(platform, status):
    """Log queue status"""
    logger.info(f"[{platform}] Queue Status: {status}")


def log_purchase_attempt(platform, sneaker_name, size):
    """Log purchase attempt"""
    logger.info(f"🛒 [{platform}] Attempting purchase: {sneaker_name} (Size: {size})")


def log_purchase_success(platform, sneaker_name, order_number=None):
    """Log successful purchase"""
    message = f"🎉 [{platform}] Successfully purchased: {sneaker_name}"
    if order_number:
        message += f" (Order: {order_number})"
    logger.info(message)


def log_purchase_failure(platform, sneaker_name, reason=None):
    """Log failed purchase"""
    message = f"❌ [{platform}] Failed to purchase: {sneaker_name}"
    if reason:
        message += f" - Reason: {reason}"
    logger.error(message)


def log_stock_alert(platform, sneaker_name):
    """Log stock availability alert"""
    logger.info(f"🔥 [{platform}] IN STOCK: {sneaker_name}")


# ========================================
# Performance Logging
# ========================================

def log_performance_metric(metric_name, value, unit="ms"):
    """Log performance metric"""
    logger.debug(f"⏱️  {metric_name}: {value:.2f} {unit}")


def log_timing(operation, duration):
    """Log operation timing"""
    logger.debug(f"⏱️  {operation} took {duration:.2f} seconds")


# ========================================
# Error Logging with Stack Trace
# ========================================

def log_exception(exception, context=None):
    """
    Log exception with full stack trace
    
    Args:
        exception: The exception object
        context: Optional context information
    """
    message = f"Exception occurred: {type(exception).__name__}: {str(exception)}"
    if context:
        message = f"[{context}] {message}"
    
    logger.exception(message)


def log_error_with_context(error_message, context_data):
    """
    Log error with additional context data
    
    Args:
        error_message: Error message
        context_data: Dictionary of context information
    """
    logger.error(f"{error_message}")
    for key, value in context_data.items():
        logger.error(f"  {key}: {value}")


# ========================================
# Session Logging
# ========================================

class SessionLogger:
    """Context manager for logging bot sessions"""
    
    def __init__(self, session_name, platform):
        self.session_name = session_name
        self.platform = platform
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        log_separator()
        logger.info(f"🎯 Starting session: {self.session_name} ({self.platform})")
        log_separator()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            logger.info(f"✅ Session completed: {self.session_name}")
        else:
            logger.error(f"❌ Session failed: {self.session_name}")
            logger.exception(f"Error: {exc_val}")
        
        logger.info(f"⏱️  Session duration: {duration:.2f} seconds")
        log_separator()
        
        # Don't suppress exceptions
        return False


# ========================================
# Statistics Logging
# ========================================

class StatisticsLogger:
    """Track and log statistics"""
    
    def __init__(self):
        self.stats = {
            'total_attempts': 0,
            'successes': 0,
            'failures': 0,
            'captchas_solved': 0,
            'captchas_failed': 0,
            'proxies_used': 0,
            'proxies_failed': 0,
        }
    
    def record_attempt(self):
        self.stats['total_attempts'] += 1
    
    def record_success(self):
        self.stats['successes'] += 1
    
    def record_failure(self):
        self.stats['failures'] += 1
    
    def record_captcha(self, success):
        if success:
            self.stats['captchas_solved'] += 1
        else:
            self.stats['captchas_failed'] += 1
    
    def record_proxy(self, success):
        self.stats['proxies_used'] += 1
        if not success:
            self.stats['proxies_failed'] += 1
    
    def get_success_rate(self):
        if self.stats['total_attempts'] == 0:
            return 0.0
        return (self.stats['successes'] / self.stats['total_attempts']) * 100
    
    def log_summary(self):
        """Log statistics summary"""
        log_separator()
        logger.info("📊 SESSION STATISTICS")
        log_separator()
        logger.info(f"Total Attempts: {self.stats['total_attempts']}")
        logger.info(f"Successes: {self.stats['successes']}")
        logger.info(f"Failures: {self.stats['failures']}")
        logger.info(f"Success Rate: {self.get_success_rate():.1f}%")
        logger.info(f"CAPTCHAs Solved: {self.stats['captchas_solved']}")
        logger.info(f"CAPTCHAs Failed: {self.stats['captchas_failed']}")
        logger.info(f"Proxies Used: {self.stats['proxies_used']}")
        logger.info(f"Proxies Failed: {self.stats['proxies_failed']}")
        log_separator()


# Create global statistics logger
stats = StatisticsLogger()


# ========================================
# Testing
# ========================================

if __name__ == "__main__":
    # Demo the logging system
    log_section("Logger Demo")
    
    log_info("This is an info message")
    log_debug("This is a debug message")
    log_warning("This is a warning message")
    log_error("This is an error message")
    log_critical("This is a critical message")
    
    log_success("Operation completed successfully")
    log_failure("Operation failed")
    
    log_separator()
    
    log_bot_action("Login", "Nike", "Using test credentials")
    log_captcha_event("Nike", "reCAPTCHA v2", True)
    log_purchase_attempt("Nike", "Air Jordan 1", "10.5")
    log_purchase_success("Nike", "Air Jordan 1", "ORD-123456")
    
    log_separator()
    
    # Demo session logging
    with SessionLogger("Nike Purchase Bot", "Nike"):
        log_info("Performing bot operations...")
        time.sleep(0.5)
        log_success("Bot operations completed")
    
    # Demo statistics
    stats.record_attempt()
    stats.record_success()
    stats.record_captcha(True)
    stats.log_summary()
