
from playwright.sync_api import sync_playwright

def test_dashboard_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8050")
        assert page.locator("text=Панель аналитики боевых событий").is_visible()
        browser.close()
