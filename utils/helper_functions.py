"""
Helper Functions for SneakerBot Ultimate
Utility functions for common bot operations
"""

import random
import string
import time
import hashlib
import json
import re
from datetime import datetime, timedelta
from faker import Faker
from user_agents import parse

fake = Faker()


# ========================================
# Email & Identity Generation
# ========================================

def generate_random_email(domain=None):
    """Generates a random email for sneaker raffle entries."""
    if domain:
        domains = [domain]
    else:
        domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"]
    
    # Generate realistic looking names
    first_name = fake.first_name().lower()
    last_name = fake.last_name().lower()
    
    # Various email patterns
    patterns = [
        f"{first_name}.{last_name}",
        f"{first_name}{last_name}",
        f"{first_name}_{last_name}",
        f"{first_name}{random.randint(100, 999)}",
        f"{first_name}.{last_name}{random.randint(10, 99)}",
    ]
    
    username = random.choice(patterns)
    email = f"{username}@{random.choice(domains)}"
    return email


def generate_random_name():
    """Generate random first and last name"""
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name()
    }


def generate_random_phone():
    """Generate random US phone number"""
    return fake.phone_number()


def generate_random_address():
    """Generate random US address"""
    return {
        "address_line1": fake.street_address(),
        "address_line2": fake.secondary_address() if random.random() > 0.7 else "",
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip_code": fake.zipcode(),
        "country": "US"
    }


# ========================================
# Browser Fingerprinting & Stealth
# ========================================

def generate_user_agent():
    """Generate random but realistic user agent"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    return random.choice(user_agents)


def generate_browser_fingerprint():
    """Generate randomized browser fingerprint data"""
    screen_resolutions = [
        (1920, 1080), (2560, 1440), (1366, 768), (1440, 900), (1536, 864)
    ]
    
    return {
        "screen_resolution": random.choice(screen_resolutions),
        "color_depth": random.choice([24, 32]),
        "timezone_offset": random.choice([-480, -420, -360, -300, -240, -180]),
        "platform": random.choice(["Win32", "MacIntel", "Linux x86_64"]),
        "language": random.choice(["en-US", "en-GB", "en-CA"]),
        "hardware_concurrency": random.choice([4, 8, 12, 16]),
        "device_memory": random.choice([4, 8, 16, 32]),
    }


def generate_canvas_fingerprint():
    """Generate unique canvas fingerprint"""
    return hashlib.md5(str(random.random()).encode()).hexdigest()


# ========================================
# Request Headers & HTTP Utilities
# ========================================

def generate_request_headers(referer=None, accept_language="en-US,en;q=0.9"):
    """Generate realistic HTTP request headers"""
    user_agent = generate_user_agent()
    
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": accept_language,
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
    }
    
    if referer:
        headers["Referer"] = referer
    
    return headers


def randomize_headers(base_headers):
    """Add randomized headers to avoid detection"""
    additional_headers = {
        "X-Requested-With": "XMLHttpRequest" if random.random() > 0.5 else None,
        "Pragma": "no-cache" if random.random() > 0.3 else None,
    }
    
    # Merge and remove None values
    merged = {**base_headers, **additional_headers}
    return {k: v for k, v in merged.items() if v is not None}


# ========================================
# Timing & Delay Functions
# ========================================

def random_delay(min_delay=1, max_delay=3):
    """Sleep for a random amount of time"""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
    return delay


def human_typing_delay(text, wpm=60):
    """Simulate human typing speed
    
    Args:
        text: The text being typed
        wpm: Words per minute (average human types 40-60 wpm)
    """
    # Calculate delay per character
    chars_per_second = (wpm * 5) / 60  # 5 chars per word average
    delay_per_char = 1 / chars_per_second
    
    total_delay = len(text) * delay_per_char
    # Add some randomness
    total_delay *= random.uniform(0.8, 1.2)
    
    return total_delay


def exponential_backoff(attempt, base_delay=1, max_delay=60):
    """Calculate exponential backoff delay
    
    Args:
        attempt: Current attempt number (starts at 0)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
    """
    delay = min(base_delay * (2 ** attempt), max_delay)
    # Add jitter
    delay *= random.uniform(0.5, 1.5)
    return delay


# ========================================
# Data Validation & Parsing
# ========================================

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate US phone number"""
    # Remove all non-digits
    digits = re.sub(r'\D', '', phone)
    return len(digits) == 10 or len(digits) == 11


def validate_zip_code(zip_code):
    """Validate US zip code"""
    pattern = r'^\d{5}(-\d{4})?$'
    return re.match(pattern, zip_code) is not None


def sanitize_sneaker_name(name):
    """Clean up sneaker name for searching"""
    # Remove special characters, normalize spaces
    cleaned = re.sub(r'[^\w\s-]', '', name)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


# ========================================
# Price & Currency Utilities
# ========================================

def parse_price(price_string):
    """Extract numeric price from string"""
    # Remove currency symbols and commas
    price_str = re.sub(r'[^\d.]', '', price_string)
    try:
        return float(price_str)
    except ValueError:
        return None


def format_price(price, currency="USD"):
    """Format price with currency symbol"""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, "$")
    return f"{symbol}{price:.2f}"


# ========================================
# Size Conversion & Formatting
# ========================================

def normalize_size(size):
    """Normalize shoe size format"""
    # Convert to string and remove spaces
    size_str = str(size).strip()
    
    # Handle European sizes
    if "EU" in size_str.upper():
        return size_str.upper()
    
    # Handle US sizes
    try:
        float_size = float(size_str)
        return str(float_size)
    except ValueError:
        return size_str


def us_to_eu_size(us_size, gender="men"):
    """Convert US shoe size to EU size"""
    conversion = {
        "men": lambda x: x + 33,
        "women": lambda x: x + 30.5,
    }
    
    converter = conversion.get(gender, conversion["men"])
    try:
        return converter(float(us_size))
    except (ValueError, TypeError):
        return None


# ========================================
# URL & Domain Utilities
# ========================================

def extract_domain(url):
    """Extract domain from URL"""
    pattern = r'https?://(?:www\.)?([^/]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None


def build_url(base_url, path, params=None):
    """Build URL with path and query parameters"""
    url = base_url.rstrip('/') + '/' + path.lstrip('/')
    
    if params:
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        url += '?' + query_string
    
    return url


# ========================================
# Web Scraping Helpers
# ========================================

def extract_site_structure(html_content):
    """Extract relevant information from HTML for bot operation"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    structure = {
        "forms": [],
        "buttons": [],
        "inputs": [],
        "links": []
    }
    
    # Extract forms
    for form in soup.find_all('form'):
        structure["forms"].append({
            "action": form.get('action'),
            "method": form.get('method'),
            "id": form.get('id'),
            "class": form.get('class')
        })
    
    # Extract buttons
    for button in soup.find_all('button'):
        structure["buttons"].append({
            "text": button.get_text(strip=True),
            "id": button.get('id'),
            "class": button.get('class'),
            "type": button.get('type')
        })
    
    # Extract inputs
    for input_field in soup.find_all('input'):
        structure["inputs"].append({
            "name": input_field.get('name'),
            "type": input_field.get('type'),
            "id": input_field.get('id'),
            "class": input_field.get('class')
        })
    
    return structure


def find_element_by_text(html_content, text, tag='button'):
    """Find HTML element by its text content"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(tag)
    
    for element in elements:
        if text.lower() in element.get_text(strip=True).lower():
            return {
                "tag": tag,
                "text": element.get_text(strip=True),
                "id": element.get('id'),
                "class": element.get('class'),
                "selector": generate_css_selector(element)
            }
    
    return None


def generate_css_selector(element):
    """Generate CSS selector for BeautifulSoup element"""
    if element.get('id'):
        return f"#{element['id']}"
    
    if element.get('class'):
        classes = '.'.join(element['class'])
        return f"{element.name}.{classes}"
    
    return element.name


# ========================================
# Security & Hashing
# ========================================

def hash_password(password, salt=None):
    """Hash password with salt"""
    if not salt:
        salt = hashlib.sha256(str(random.random()).encode()).hexdigest()[:16]
    
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${hashed.hex()}"


def verify_password(password, hashed):
    """Verify password against hash"""
    try:
        salt, hash_value = hashed.split('$')
        return hash_password(password, salt) == hashed
    except ValueError:
        return False


def generate_session_token():
    """Generate random session token"""
    return hashlib.sha256(str(time.time()).encode()).hexdigest()


# ========================================
# File & Path Utilities
# ========================================

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    import os
    os.makedirs(path, exist_ok=True)
    return path


def generate_filename(prefix, extension, include_timestamp=True):
    """Generate unique filename"""
    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
    return f"{prefix}.{extension}"


def save_screenshot(driver, filename=None):
    """Save screenshot with automatic naming"""
    if not filename:
        filename = generate_filename("screenshot", "png")
    
    ensure_directory("screenshots")
    filepath = f"screenshots/{filename}"
    driver.save_screenshot(filepath)
    return filepath


# ========================================
# Data Serialization
# ========================================

def serialize_to_json(data, filepath):
    """Save data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def deserialize_from_json(filepath):
    """Load data from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


# ========================================
# Performance & Monitoring
# ========================================

def measure_execution_time(func):
    """Decorator to measure function execution time"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"⏱️  {func.__name__} executed in {execution_time:.2f} seconds")
        return result
    return wrapper


def calculate_success_rate(successes, total_attempts):
    """Calculate success rate percentage"""
    if total_attempts == 0:
        return 0.0
    return (successes / total_attempts) * 100


# ========================================
# Text Processing
# ========================================

def truncate_string(text, max_length=50, suffix="..."):
    """Truncate string to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def clean_whitespace(text):
    """Clean and normalize whitespace"""
    return ' '.join(text.split())


# ========================================
# Testing & Debug Utilities
# ========================================

def generate_test_data():
    """Generate complete test data set"""
    return {
        "account": {
            "email": generate_random_email(),
            "password": "TestPassword123!",
            **generate_random_name(),
            "phone": generate_random_phone()
        },
        "address": generate_random_address(),
        "payment": {
            "card_number": "4111111111111111",  # Test card
            "cvv": "123",
            "expiry_month": "12",
            "expiry_year": "2025"
        }
    }


def print_test_data():
    """Print formatted test data"""
    data = generate_test_data()
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    # Demo the helper functions
    print("=" * 50)
    print("Helper Functions Demo")
    print("=" * 50)
    
    print("\n📧 Random Email:", generate_random_email())
    print("👤 Random Name:", generate_random_name())
    print("📱 Random Phone:", generate_random_phone())
    print("🏠 Random Address:", generate_random_address())
    print("\n🌐 User Agent:", generate_user_agent())
    print("🖥️  Browser Fingerprint:", generate_browser_fingerprint())
    
    print("\n" + "=" * 50)
    print("Test Data Set:")
    print("=" * 50)
    print_test_data()
