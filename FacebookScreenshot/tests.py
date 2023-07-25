# from playwright.sync_api import sync_playwright
#
#
# def run():
#     playwright = sync_playwright().start()
#     chromium = playwright.chromium  # or "firefox" or "webkit".
#     browser = chromium.launch(
#         proxy={'server': 'http://127.0.0.1:19180'},
#         headless=True)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto(r"https://www.facebook.com/groups/1673433336025800/about")
#     e = page.locator("div[aria-label='Accessible login button']")
#     print(e)
#     browser.close()
#
#
# run()


