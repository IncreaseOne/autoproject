import asyncio

from django.test import TestCase

# Create your tests here.
from playwright.async_api import async_playwright


async def run():
    async with async_playwright() as playwright:
        chromium = playwright.chromium  # or "firefox" or "webkit".
        browser = await chromium.launch(
            headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("D:/vue_test/%E6%AD%A3%E5%88%99%E5%AD%A6%E4%B9%A0/%E5%8C%B9%E9%85%8D%E6%96%87%E6%9C%AC.html")
        role = page.get_by_role(role="article")
        print(role)
        await browser.close()

asyncio.run(run())

