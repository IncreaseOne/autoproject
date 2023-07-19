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
from untils.awss3 import S3

class AutoScreenshot():
    main_page = "https://www.facebook.com"
    proxy = {"server": "http://127.0.0.1:19180"}
    account = {"username": "czh18030315579@gmail.com", "password": "chen.1314520"}

    def __init__(self, code=None):
        self.code = code
        self.results = []

    async def login(self, context, account: dict):
        page = await context.new_page()
        await page.goto(self.main_page)
        await page.type("#email", account.get("username"))
        await page.type("#pass", account.get("password"))
        await page.click("//button[@name='login']")
        await expect(page.get_by_label("首页")).to_be_visible(timeout=20000)
        await context.storage_state(path=f"{BASE_DIR}/login_data_facebook.json")
        await page.close()
        return context

    async def screenshot(self, context):

        page = await context.new_page()
        await page.goto(f'https://www.facebook.com/search/top/?q={self.code}', wait_until="domcontentloaded")
        logging.info(f"{self.code}: 页面渲染完成")
        if await page.get_by_text("展开").count() > 0:
            expands = await page.get_by_text("展开").all()
            for i in expands:
                try:
                    await i.click()
                except:
                    pass
        while await page.locator("a", has_text="了解更多").is_visible(timeout=3000) is False:
            await page.mouse.wheel(0, 500)
            if await page.get_by_text("展开").count() > 0:
                expands = await page.get_by_text("展开").all()
                for i in expands:
                    try:
                        await i.click(timeout=3000)
                    except:
                        pass
        logging.info(f"{self.code}: 页面展开到底部")
        await page.mouse.wheel(0, 0)
        logger.info(f"{self.code}: 页面回到顶部")
        need_to_screenshot = await page.get_by_role(role="article").filter(has_text=re.compile(f".*{self.code}.*")).all()
        for i in need_to_screenshot:
            global screenshot_bytes
            global link
            try:
                await i.scroll_into_view_if_needed()
                screenshot_bytes = await i.screenshot()
                link = await i.get_by_role("link").first.get_attribute("href")
            except Exception as e:
                logger.error("{}查找link失败:{}".format(self.code, e))
            self.results.append(S3().upload_single_file({"link": link, "image": screenshot_bytes}, f"{time.time()}.png"))
        logger.info(f"{self.code}: 任务全部完成")
        await page.close()

    async def start_screenshot(self):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(
                headless=True)
            now_time = time.time()
            with open(f"{BASE_DIR}/login_data_facebook.json", mode="r") as f:
                obj = json.load(f)
                expires = obj["cookies"][1]["expires"]
            # 如果过期时间小于现在时间，重新登录
            if now_time > expires:
                context = await self.login(await browser.new_context(viewport={"width": 1080, "height": 1920}), account=self.account)
            else:
                context = await browser.new_context(storage_state=f"{BASE_DIR}/login_data_facebook.json", viewport={"width": 1080, "height": 1920})
            await self.screenshot(context)
            await context.close()
            await browser.close()
            return self.results


    async def start_login(self):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(
                headless=True)
            context = await browser.new_context()
            await self.login(context=context, account=self.account)


