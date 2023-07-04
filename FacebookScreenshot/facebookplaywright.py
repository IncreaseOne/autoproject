# -*- coding: utf-8 -*-
# author：王勇
import asyncio
import base64
import json
import os
import re
import time
import logging
from playwright.async_api import async_playwright, expect

logger = logging.getLogger(__name__)
from AutoTestCode.settings import BASE_DIR
import queue


class AutoScreenshot():
    USERNAME = "czh18030315579@gmail.com"
    PASSWORD = "chen.1314520"
    main_page = "https://www.facebook.com"

    def __init__(self, code):
        self.code = code
        self.results = []

    async def login(self, context, account: dict):
        page = await context.new_page()
        await page.goto(self.main_page)
        await page.fill("#email", account.get("username"))
        await page.fill("#pass", account.get("password"))
        await page.click("//button[@name='login']")
        await expect(page.get_by_label("首页")).to_be_visible(timeout=20000)
        await page.close()
        return context.cookies()

    async def screenshot(self, context):
        page = await context.new_page()
        await page.goto(f'https://www.facebook.com/search/top/?q={self.code}', wait_until="domcontentloaded")
        # try:
        #     await expect(page.get_by_role(role="article").first).to_have_text(re.compile())
        # except:
        #     return False
        # 点击展开
        if await page.get_by_text("展开").count() > 0:
            zankai = await page.get_by_text("展开").all()
            for i in zankai:
                try:
                    await i.click()
                except:
                    pass
        while await page.locator("a", has_text="了解更多").is_visible(timeout=3000) is False:
            await page.mouse.wheel(0, 500)
            if await page.get_by_text("展开").count() > 0:
                zankai = await page.get_by_text("展开").all()
                for i in zankai:
                    try:
                        await i.click(timeout=3000)
                    except:
                        pass
        need_to_screenshot = await page.get_by_role(role="article").filter(has_text=re.compile(f".*{self.code}.*")).all()
        for i in need_to_screenshot:
            #await i.scroll_into_view_if_needed(timeout=30000)
            screenshot_bytes = await i.screenshot()
            self.results.append(base64.b64encode(screenshot_bytes).decode("utf-8"))
        await page.close()

    async def run(self):
            playwright = await async_playwright().start()
            chromium = playwright.chromium
            browser = await chromium.launch(
                headless=True)
                # proxy={"server": "http://127.0.0.1:19180"})
            context = await browser.new_context(storage_state=f"{BASE_DIR}/login_data_facebook.json", viewport={"width": 1080, "height": 1920})
            await self.screenshot(context)

            await context.close()
            await browser.close()
            return self.results

    # async def login_account(self, accounts: list):
    #     q = queue.Queue()
    #     for account in accounts:
    #         q.put(account)
    #     async with async_playwright() as playwright:
    #         chromium = playwright.chromium
    #         browser = await chromium.launch(
    #             proxy={"server": "http://127.0.0.1:19180"})
    #         context = await browser.new_context()
    #         tasks = []
    #         while True:
    #             if not q
    #                 for i in range(0, 5):
    #                     account = q.get()
    #                     tasks.append(self.login(context, account))
    #             else:
    #                 if q.empty():
    #                     logger.info("全部账号登录成功")
    #                     break;
    #                 else:
    #                     for i in range(0, q.qsize()):
    #                         account = q.get()
    #                         tasks.append(self.login(context, account))




