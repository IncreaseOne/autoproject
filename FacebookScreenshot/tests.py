from playwright.sync_api import sync_playwright


def run():
    playwright = sync_playwright().start()
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(
        headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com")
    browser.close()


run()




