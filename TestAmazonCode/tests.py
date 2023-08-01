import asyncio
import json
import re

from django.test import TestCase

# Create your tests here.
# import requests
from playwright.async_api import async_playwright


async def do_task():
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch(headless=False)
        context = await browser.new_context(
            ignore_https_errors=True,
            viewport={"width": 1000, "height": 680},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
            # storage_state= f"{BASE_DIR}/TestAmazonCode/login_amazon_com.json"
        )
        # with open(f"{BASE_DIR}/TestAmazonCode/login_amazon_com.json", mode="r") as f:
        #     self.storage = json.load(f)
        # 先登录，通过上下文缓存登录状态
        page = await context.new_page()
        await page.goto(r"D:\vue_test\正则学习\匹配文本.html", timeout=50000, wait_until="domcontentloaded")
        if await page.locator(".nav-bb-right > a").first.is_visible():
            print("进入非正常页面，正在处理")
            await page.locator(".nav-bb-right > a").first.click()
        if await page.locator(".a-column.a-span-last.a-text-right").is_visible():
            print("需要输入验证码，正在处理...")
            await page.locator(".a-column.a-span-last.a-text-right").click()
        print("成功进入amazon主页")

asyncio.run(do_task())