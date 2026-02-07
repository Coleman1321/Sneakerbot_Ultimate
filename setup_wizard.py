#!/usr/bin/env python3
"""
SneakerBot Ultimate - Setup Wizard
Interactive setup for first-time users
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def check_python_version():
    """Check Python version"""
    print_info("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} - Need 3.8+")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print_info("Installing Python dependencies...")
    
    try:
        # Install minimal required packages
        packages = [
            "playwright",
            "requests",
            "faker",
            "python-dotenv",
        ]
        
        for package in packages:
            print(f"  Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package, "-q"], 
                         check=True, capture_output=True)
        
        print_success("Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False

def install_playwright_browsers():
    """Install Playwright browsers"""
    print_info("Installing Playwright browsers (Chromium)...")
    
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], 
                      check=True)
        print_success("Playwright browsers installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install browsers: {e}")
        return False

def initialize_database():
    """Initialize database"""
    print_info("Initializing database...")
    
    try:
        subprocess.run([sys.executable, "database/init_db.py"], check=True)
        print_success("Database initialized")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to initialize database: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    print_info("Creating configuration file...")
    
    if os.path.exists(".env"):
        print_warning(".env already exists, skipping")
        return True
    
    try:
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as f:
                content = f.read()
            
            # Ask user for optional config
            print("\n  Optional: Enter API keys (press Enter to skip)")
            captcha_key = input("  2Captcha API Key (optional): ").strip()
            discord_webhook = input("  Discord Webhook URL (optional): ").strip()
            
            if captcha_key:
                content = content.replace("your_2captcha_api_key_here", captcha_key)
            if discord_webhook:
                content = content.replace("https://discord.com/api/webhooks/your_webhook_here", discord_webhook)
            
            # Set dry run mode by default
            content = content.replace("DRY_RUN=True", "DRY_RUN=False")
            
            with open(".env", "w") as f:
                f.write(content)
            
            print_success("Configuration file created")
            return True
        else:
            print_warning(".env.example not found, skipping")
            return True
    except Exception as e:
        print_error(f"Failed to create .env: {e}")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut"""
    print_info("Creating desktop shortcut...")
    
    system = platform.system()
    current_dir = os.getcwd()
    
    try:
        if system == "Windows":
            # Create Windows shortcut
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "SneakerBot Ultimate.lnk"
            
            # Create .bat file to launch
            bat_content = f"""@echo off
cd /d "{current_dir}"
"{sys.executable}" run_bot.py
pause
"""
            bat_path = os.path.join(current_dir, "launch_sneakerbot.bat")
            with open(bat_path, "w") as f:
                f.write(bat_content)
            
            print_success(f"Created launcher: {bat_path}")
            print_info("Double-click launch_sneakerbot.bat to run")
            
        elif system == "Darwin":  # macOS
            # Create .command file
            desktop = Path.home() / "Desktop"
            command_path = desktop / "SneakerBot Ultimate.command"
            
            command_content = f"""#!/bin/bash
cd "{current_dir}"
"{sys.executable}" run_bot.py
"""
            with open(command_path, "w") as f:
                f.write(command_content)
            
            os.chmod(command_path, 0o755)
            print_success(f"Created launcher: {command_path}")
            
        else:  # Linux
            # Create .desktop file
            desktop = Path.home() / "Desktop"
            desktop_path = desktop / "sneakerbot-ultimate.desktop"
            
            desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=SneakerBot Ultimate
Comment=Security Research Bot
Exec={sys.executable} {current_dir}/run_bot.py
Path={current_dir}
Icon={current_dir}/icon.png
Terminal=true
Categories=Development;
"""
            with open(desktop_path, "w") as f:
                f.write(desktop_content)
            
            os.chmod(desktop_path, 0o755)
            print_success(f"Created launcher: {desktop_path}")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to create shortcut: {e}")
        print_info("You can manually run: python run_bot.py")
        return False

def create_quick_launch_script():
    """Create quick launch scripts"""
    print_info("Creating quick launch script...")
    
    system = platform.system()
    
    if system == "Windows":
        script_name = "START_HERE.bat"
        content = f"""@echo off
title SneakerBot Ultimate
cd /d "%~dp0"
"{sys.executable}" run_bot.py
pause
"""
    else:
        script_name = "START_HERE.sh"
        content = f"""#!/bin/bash
cd "$(dirname "$0")"
"{sys.executable}" run_bot.py
"""
    
    with open(script_name, "w") as f:
        f.write(content)
    
    if system != "Windows":
        os.chmod(script_name, 0o755)
    
    print_success(f"Created: {script_name}")
    return True

def main():
    """Main setup wizard"""
    print_header("SneakerBot Ultimate - Setup Wizard")
    
    print("Welcome to SneakerBot Ultimate!")
    print("This wizard will help you set up everything.\n")
    
    input("Press Enter to begin setup...")
    
    # Step 1: Check Python
    print_header("Step 1/6: Checking Python")
    if not check_python_version():
        print_error("Please install Python 3.8 or higher")
        return
    
    # Step 2: Install dependencies
    print_header("Step 2/6: Installing Dependencies")
    if not install_dependencies():
        print_error("Setup failed at dependency installation")
        return
    
    # Step 3: Install browsers
    print_header("Step 3/6: Installing Browsers")
    if not install_playwright_browsers():
        print_warning("Browser installation failed, but continuing...")
    
    # Step 4: Initialize database
    print_header("Step 4/6: Setting Up Database")
    if not initialize_database():
        print_error("Setup failed at database initialization")
        return
    
    # Step 5: Create config
    print_header("Step 5/6: Configuration")
    create_env_file()
    
    # Step 6: Create shortcuts
    print_header("Step 6/6: Creating Shortcuts")
    create_quick_launch_script()
    create_desktop_shortcut()
    
    # Success!
    print_header("Setup Complete!")
    print_success("SneakerBot Ultimate is ready to use!\n")
    
    print("📋 Next Steps:")
    print("  1. Double-click START_HERE to launch the bot")
    print("  2. Or run: python run_bot.py")
    print("  3. Add your accounts in the GUI")
    print("  4. Configure settings as needed\n")
    
    print("📚 Documentation:")
    print("  - README.md - Complete guide")
    print("  - QUICK_START.md - Quick reference")
    print("  - docs/SECURITY_ANALYSIS.md - Security research\n")
    
    print_info("For your presentation, focus on the security analysis!")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
    except Exception as e:
        print_error(f"Setup failed: {e}")
        import traceback
        traceback.print_exc()
