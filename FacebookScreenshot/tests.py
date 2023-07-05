import asyncio

from playwright.async_api import async_playwright


async def run():
    async with async_playwright() as playwright:
        chromium = playwright.chromium  # or "firefox" or "webkit".
        browser = await chromium.launch(
            headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.baidu.com")
        await browser.close()
        print("success")
asyncio.run(run())



