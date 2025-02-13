from playwright.sync_api import sync_playwright
from src.proxy_manager import get_random_proxy
from src.captcha_solver import solve_captcha
import time

NIKE_LOGIN_URL = "https://www.nike.com/login"

def nike_login(email, password):
    """Logs into Nike account using Playwright"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        proxy = get_random_proxy()
        if proxy:
            page = browser.new_page(proxy={"server": proxy})
        else:
            page = browser.new_page()  # ✅ No proxy if unavailable
        page.goto(NIKE_LOGIN_URL)

        # Enter login details
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')

        time.sleep(5)  # Wait for authentication

        # Handle CAPTCHA if required
        if page.locator('iframe[title="reCAPTCHA"]').count() > 0:
            site_key = page.get_attribute('iframe[title="reCAPTCHA"]', "data-sitekey")
            captcha_solution = solve_captcha(site_key, NIKE_LOGIN_URL)
            if captcha_solution:
                page.fill('textarea[name="g-recaptcha-response"]', captcha_solution)

        time.sleep(2)
        return page

def enter_snkrs_draw(page, sneaker_id, size):
    """Automates SNKRS draw entry"""
    draw_url = f"https://www.nike.com/launch/t/{sneaker_id}"
    page.goto(draw_url)
    page.select_option('select[name="size"]', size)
    page.click("button.join-draw")
    time.sleep(3)
    return True
