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

    def __init__(self, code=None):
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
                zankai = await page.get_by_text("展开").all()
                for i in zankai:
                    try:
                        await i.click(timeout=3000)
                    except:
                        pass
        logging.info(f"{self.code}: 页面展开到底部")
        need_to_screenshot = await page.get_by_role(role="article").filter(has_text=re.compile(f".*{self.code}.*")).all()
        for i in need_to_screenshot:
            screenshot_bytes = await i.screenshot()
            try:
                link = await i.get_by_role("link").first.get_attribute("href")
            except:
                link = None
            self.results.append(S3().upload_single_file({"link": link, "image": screenshot_bytes}, f"{time.time()}.png"))
        logger.info(f"{self.code}: 任务全部完成")
        await page.close()

    async def start_screenshot(self):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(
                headless=True)
            context = await browser.new_context(storage_state=f"{BASE_DIR}/login_data_facebook.json", viewport={"width": 1080, "height": 1920})
            await self.screenshot(context)
            await context.close()
            await browser.close()
            return self.results

    async def update_link(self, context, link_obj: dict):
        page = await context.new_page()
        try:
            groups_link = await page.get_by_role("article").first.get_by_role("link").first.get_attribute("href")
            groups_id = re.search("/groups/.+/", groups_link).group()
            new_link = f"https://www.facebook.com{groups_id}"
            link_obj["link"] = new_link
            return link_obj
        except:
            logger.info("{}获取失败".format(link_obj.get("link")))
            return link_obj

    # 更正群组链接
    async def get_real_groups_link(self, links: list):
        q = queue.Queue()
        for link in links:
            q.put(link)
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(
                )
            context = await browser.new_context()
            tasks = []
            while True:
                if not q:
                    for i in range(0, 5):
                        link_obj = q.get()
                        tasks.append(self.update_link(context, link_obj))
                else:
                    if q.empty():
                        logger.info("全部更替完成")
                        break;
                    else:
                        for i in range(0, q.qsize()):
                            link_obj = q.get()
                            tasks.append(self.update_link(context, link_obj))




