# 🤖 SneakerBot Ultimate - Security Research Project

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Research](https://img.shields.io/badge/Purpose-Security%20Research-red.svg)]()

> **⚠️ DISCLAIMER**: This project is developed exclusively for security research and educational purposes. It demonstrates bot attack vectors on e-commerce platforms to help companies build better defenses. Unauthorized use of this software to circumvent website terms of service or for commercial gain is strictly prohibited and may be illegal.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Security Research Purpose](#security-research-purpose)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Bot Capabilities](#bot-capabilities)
- [Attack Vectors Demonstrated](#attack-vectors-demonstrated)
- [Defensive Countermeasures](#defensive-countermeasures)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [Legal & Ethics](#legal--ethics)
- [License](#license)

---

## 🎯 Project Overview

**SneakerBot Ultimate** is a comprehensive bot framework that demonstrates automated purchasing behaviors on sneaker/streetwear e-commerce platforms. This project was commissioned by a coalition of sneaker and streetwear companies to understand bot attack vectors and develop more effective security measures.

### Key Objectives

1. **Educational**: Demonstrate how bots operate to help developers and security teams
2. **Defensive**: Identify vulnerabilities in current anti-bot measures
3. **Research**: Analyze success rates of various bot techniques
4. **Documentation**: Provide detailed reports on attack patterns

---

## 🔒 Security Research Purpose

This bot framework serves as a "red team" tool for security research, specifically designed to:

- **Demonstrate** common bot attack patterns
- **Test** anti-bot defenses (CAPTCHA, rate limiting, queue systems)
- **Analyze** detection mechanisms and their effectiveness
- **Document** best practices for bot prevention
- **Educate** security teams on emerging bot techniques

### Intended Use Cases

✅ Security testing with explicit permission  
✅ Academic research on bot behavior  
✅ Defense mechanism development  
✅ Educational demonstrations  
✅ Company-sanctioned penetration testing  

❌ Unauthorized automated purchasing  
❌ Circumventing terms of service  
❌ Commercial bot operations  
❌ Resale operations  

---

## ✨ Features

### 🤖 Multi-Platform Support

- **Nike/SNKRS** - Full automation including draw entries
- **Adidas** - Queue handling, Yeezy releases
- **Shopify** - Universal Shopify store support
- **Footsites** - FootLocker, Champs, Eastbay
- **Supreme** - High-speed checkout
- **JD Sports/Finish Line/DSG** - Additional platform support

### 🛡️ Stealth & Evasion

- **Browser Fingerprint Randomization** - Unique fingerprints per session
- **Proxy Rotation** - Automatic IP rotation with testing
- **Human-Like Behavior** - Randomized delays and typing patterns
- **Anti-Detection** - Stealth browsing modes
- **Session Management** - Persistent cookies and tokens

### 🧩 Advanced Features

- **CAPTCHA Solving** - Integration with 2Captcha/AntiCaptcha
- **Queue Monitoring** - Automatic queue detection and waiting
- **Stock Monitoring** - Real-time inventory tracking
- **Raffle Entry** - Multi-entry raffle automation
- **Account Management** - Multi-account support with SQLite database
- **Notifications** - Discord/Telegram alerts
- **AI Auto-Fix** - Adaptive bot behavior using AI

### 📊 Analytics & Reporting

- **Performance Metrics** - Success rates, timing analysis
- **Error Logging** - Comprehensive error tracking
- **Security Reports** - Automated defense analysis
- **Statistics Dashboard** - Real-time bot performance

---

## 🏗️ Architecture

```
sneakerbot_complete/
├── config/                    # Configuration files
│   ├── settings.py           # Main configuration
│   ├── proxies.txt           # Proxy list
│   └── __init__.py
│
├── database/                  # Data storage
│   ├── init_db.py            # Database initialization
│   └── userdata.db           # SQLite database
│
├── src/                       # Core bot implementations
│   ├── nike_bot.py           # Nike/SNKRS bot
│   ├── adidas_bot.py         # Adidas bot
│   ├── shopify_bot.py        # Shopify bot
│   ├── supreme_bot.py        # Supreme bot
│   ├── footsites_bot.py      # Footsites bot
│   ├── jd_finish_dsg_bot.py  # JD/Finish/DSG bot
│   ├── raffle_bot.py         # Raffle entry bot
│   ├── stock_monitor.py      # Stock monitoring
│   ├── captcha_solver.py     # CAPTCHA handling
│   ├── proxy_manager.py      # Proxy rotation
│   ├── account_manager.py    # Account management
│   ├── checkout_manager.py   # Checkout automation
│   ├── notifications.py      # Alert system
│   ├── ai_auto_fix.py        # AI-powered adaptation
│   └── rollback_manager.py   # Version control
│
├── utils/                     # Utility functions
│   ├── helper_functions.py   # Common utilities
│   └── logger.py             # Logging system
│
├── gui/                       # User interface
│   └── main.py               # Tkinter GUI
│
├── docs/                      # Documentation
│   ├── SECURITY_ANALYSIS.md  # Security research report
│   ├── API.md                # API documentation
│   └── DEFENSIVE_MEASURES.md # Countermeasures guide
│
├── tests/                     # Test suite
│   ├── test_bots.py
│   └── test_utilities.py
│
├── backup/                    # Backup directory
├── screenshots/               # Screenshot storage
├── logs/                      # Log files
│
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── run_bot.py                # Main entry point
└── .env.example              # Environment variables template

```

---

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser
- pip (Python package manager)
- Git (for cloning repository)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/sneakerbot-ultimate.git
cd sneakerbot-ultimate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Playwright Browsers

```bash
playwright install chromium
```

### Step 4: Initialize Database

```bash
python database/init_db.py
```

### Step 5: Configure Settings

```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# CAPTCHA Services
CAPTCHA_API_KEY=your_2captcha_api_key_here
ANTICAPTCHA_API_KEY=your_anticaptcha_api_key_here

# Notifications
DISCORD_WEBHOOK=your_discord_webhook_url_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# AI Services (Optional)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Development
DEBUG_MODE=False
DRY_RUN=True
```

### Proxy Configuration

Create `config/proxies.txt` with your proxies (one per line):

```
http://username:password@proxy1.example.com:8080
http://username:password@proxy2.example.com:8080
socks5://username:password@proxy3.example.com:1080
```

### Settings Customization

Edit `config/settings.py` to customize:

- Bot behavior and timing
- Platform-specific settings
- Retry logic and error handling
- Notification preferences
- Performance tuning

---

## 🚀 Usage

### Quick Start

```python
from src.nike_bot import nike_purchase

# Purchase a sneaker
success = nike_purchase(
    email="your@email.com",
    password="your_password",
    sneaker_name="Air Jordan 1",
    size="10.5",
    use_proxy=True
)
```

### GUI Application

```bash
python run_bot.py
```

### Command Line Interface

```bash
# Nike purchase
python -m src.nike_bot --email user@example.com --password pass123 --sneaker "Jordan 1" --size 10

# SNKRS draw entry
python -m src.nike_bot --mode draw --product-url https://nike.com/... --size 10

# Stock monitoring
python -m src.stock_monitor --platform Nike --keywords "Jordan,Dunk" --notify
```

### Python API

```python
from src.nike_bot import NikeBot
from src.account_manager import get_account_manager

# Get account
am = get_account_manager()
account = am.get_random_account("Nike")

# Run bot
with NikeBot(account["email"], account["password"]) as bot:
    if bot.login():
        bot.complete_purchase("Air Jordan 1", "10.5")
```

---

## 🎯 Bot Capabilities

### Nike/SNKRS Bot

- ✅ Account login with stealth mode
- ✅ Product search and navigation
- ✅ Size selection automation
- ✅ SNKRS draw entry
- ✅ CAPTCHA solving integration
- ✅ Checkout automation
- ✅ Queue detection and handling

### Adidas Bot

- ✅ Login automation
- ✅ Queue monitoring and bypass attempts
- ✅ Product search
- ✅ Size selection
- ✅ Add to cart automation
- ✅ Yeezy release support

### Shopify Bot

- ✅ Universal Shopify support
- ✅ Stock monitoring via product.json
- ✅ Cart API utilization
- ✅ Fast checkout
- ✅ Multiple store support

### Additional Features

- 🔄 Automatic proxy rotation
- 🧩 CAPTCHA solving (2Captcha/AntiCaptcha)
- 📊 Real-time stock monitoring
- 🎲 Raffle entry automation
- 📧 Multi-account management
- 🔔 Discord/Telegram notifications
- 🤖 AI-powered auto-fix
- 📈 Performance analytics

---

## 🎯 Attack Vectors Demonstrated

This project demonstrates the following bot attack techniques:

### 1. Browser Automation Exploitation
- Headless browser usage
- Automation framework detection bypass
- WebDriver signature removal

### 2. Fingerprint Randomization
- Browser fingerprint spoofing
- Canvas fingerprint randomization
- WebGL fingerprint modification
- Screen resolution spoofing

### 3. Network-Level Evasion
- Proxy rotation
- IP address randomization
- Request header manipulation
- User-agent rotation

### 4. Behavioral Mimicry
- Human-like typing patterns
- Randomized delays
- Natural mouse movements
- Realistic session patterns

### 5. CAPTCHA Circumvention
- Third-party solver integration
- Audio CAPTCHA exploitation
- Machine learning-based solving

### 6. Rate Limiting Evasion
- Request throttling
- Distributed requests across proxies
- Session token rotation
- Cookie management

### 7. Queue System Bypass
- Queue detection
- Waiting automation
- Refresh strategies

---

## 🛡️ Defensive Countermeasures

Based on this research, recommended defenses include:

### Detection Techniques

1. **Browser Fingerprinting**
   - Analyze canvas/WebGL fingerprints
   - Check for automation markers
   - Validate browser consistency

2. **Behavioral Analysis**
   - Mouse movement tracking
   - Keystroke dynamics
   - Session duration analysis
   - Navigation patterns

3. **Network Analysis**
   - IP reputation scoring
   - Proxy detection
   - Request rate monitoring
   - Geographic anomaly detection

### Prevention Measures

1. **CAPTCHA Implementation**
   - Strategic placement (before checkout)
   - Progressive difficulty
   - Multiple CAPTCHA types
   - Invisible reCAPTCHA

2. **Rate Limiting**
   - Per-IP rate limits
   - Per-session rate limits
   - Progressive delays
   - Temporary IP blocks

3. **Queue Systems**
   - Fair queuing algorithms
   - Random queue assignment
   - Queue bypass detection
   - Virtual waiting rooms

4. **Account Verification**
   - Email verification
   - Phone verification
   - Purchase history checks
   - Account age requirements

5. **Checkout Protection**
   - Address verification
   - Payment method validation
   - Purchase velocity limits
   - Shipping address validation

See `docs/DEFENSIVE_MEASURES.md` for detailed implementation guides.

---

## 📚 API Documentation

### NikeBot Class

```python
from src.nike_bot import NikeBot

bot = NikeBot(email, password, use_proxy=True)
bot.setup_browser()        # Initialize browser
bot.login()                # Login to account
bot.search_sneaker(name)   # Search for product
bot.select_size(size)      # Select shoe size
bot.add_to_cart()          # Add to cart
bot.go_to_checkout()       # Navigate to checkout
bot.enter_snkrs_draw(url, size)  # Enter SNKRS draw
bot.cleanup()              # Close browser
```

### ProxyManager

```python
from src.proxy_manager import ProxyManager

pm = ProxyManager()
proxy = pm.get_random_proxy()      # Get random proxy
proxy = pm.get_working_proxy()     # Get tested proxy
pm.test_proxy(proxy)               # Test specific proxy
```

### AccountManager

```python
from src.account_manager import AccountManager

am = AccountManager()
account_id = am.create_account("Nike")     # Create account
account = am.get_account("Nike")           # Get account
account = am.get_random_account("Nike")    # Get random account
am.update_last_used(account_id)            # Update timestamp
```

See `docs/API.md` for complete API reference.

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_bots.py

# Run with coverage
pytest --cov=src tests/
```

---

## 📊 Performance Metrics

This bot framework includes built-in performance tracking:

- Success rate calculation
- Average execution time
- CAPTCHA solve rate
- Proxy success rate
- Error frequency analysis

View statistics:

```python
from utils.logger import stats

stats.log_summary()  # Print statistics
```

---

## 🤝 Contributing

This is a security research project. Contributions should focus on:

- ✅ Improving detection evasion research
- ✅ Documenting new attack vectors
- ✅ Enhancing defensive measures documentation
- ✅ Bug fixes and code quality
- ✅ Test coverage improvements

Please read `CONTRIBUTING.md` before submitting pull requests.

---

## ⚖️ Legal & Ethics

### Terms of Use

This software is provided for **educational and security research purposes only**.

By using this software, you agree to:

1. **Only use it with explicit permission** from website owners
2. **Not circumvent terms of service** of any website
3. **Not use it for commercial gain** or resale operations
4. **Take responsibility** for your own use of this software
5. **Respect intellectual property** and website policies

### Disclaimer

The developers of this software:

- Are NOT responsible for misuse of this software
- Do NOT endorse violating terms of service
- Do NOT support commercial bot operations
- PROVIDE this for educational purposes only

### Legal Compliance

Users are responsible for ensuring compliance with:

- Local laws and regulations
- Website terms of service
- Anti-bot legislation (e.g., BOTS Act in the US)
- Computer fraud and abuse laws

**Unauthorized use may result in:**
- Account termination
- IP bans
- Legal action
- Criminal charges in some jurisdictions

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 SneakerBot Ultimate Research Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software for educational and security research purposes only...
```

---

## 📞 Contact

For security research inquiries:
- Email: security@example.com
- GitHub Issues: [Project Issues](https://github.com/yourusername/sneakerbot-ultimate/issues)

For responsible disclosure of vulnerabilities:
- Email: security@example.com
- PGP Key: [Public Key](security-key.asc)

---

## 🙏 Acknowledgments

- Sneaker/streetwear coalition partners for supporting this research
- Security researchers in the anti-bot community
- Open-source contributors to Playwright, Selenium, and related projects
- Academic institutions studying bot behavior

---

## 📖 Further Reading

- [OWASP Bot Management](https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks)
- [Bot Detection Best Practices](https://example.com)
- [Anti-Bot Technologies Overview](https://example.com)
- [Web Automation Ethics](https://example.com)

---

<p align="center">
  <strong>⚠️ Use Responsibly | 🔒 For Security Research Only | 📚 Educational Purpose</strong>
</p>
