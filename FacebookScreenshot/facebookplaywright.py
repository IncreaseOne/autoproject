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
from apscheduler.schedulers.background import BackgroundScheduler
from AutoTestCode.settings import BASE_DIR

logger = logging.getLogger(__name__)

import queue

class AutoScreenshot():
    main_page = "https://www.facebook.com"
    proxy = {"server": "http://127.0.0.1:19180"}
    account = {"username": "czh18030315579@gmail.com", "password": "chen.1314520"}

    def __init__(self, search=None, orderId=None):
        self.search = search
        self.results = []
        self.orderId = orderId

    async def login(self, context, account: dict):
        logger.info("开始登录")
        page = await context.new_page()
        await page.goto(self.main_page)
        await page.type("#email", account.get("username"))
        await page.type("#pass", account.get("password"))
        await page.click("//button[@name='login']")
        await expect(page.locator("a[aria-label='首页']")).to_be_visible(timeout=20000)
        await context.storage_state(path=f"{BASE_DIR}/login_data/login_data_facebook.json")
        await page.close()
        logger.info("登录成功")
        return context

    async def screenshot(self, context):

        page = await context.new_page()
        await page.goto(f'https://www.facebook.com/search/posts/?q={self.search}&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D')
        logging.info(f"{self.search}: 页面渲染完成")
        if await page.get_by_text("展开").count() > 0:
            expands = await page.get_by_text("展开").all()
            for i in expands:
                try:
                    await i.click()
                except:
                    pass
        move_wheel_before = time.time()
        while await page.locator("span", has_text=re.compile(".*已经到底啦~.*|.*找不到任何结果.*|.*加入或登录 Facebook.*|.*你的帐户已锁定.*")).is_visible(timeout=3000) is False:
            await page.mouse.wheel(0, 500)
            if await page.get_by_text("展开").count() > 0:
                expands = await page.get_by_text("展开").all()
                for i in expands:
                    try:
                        await i.click(timeout=3000)
                    except:
                        pass
            elif time.time() - move_wheel_before > 300:
                return False

        logging.info(f"{self.search}: 页面展开到底部")
        await page.mouse.wheel(0, 0)
        logger.info(f"{self.search}: 页面回到顶部")
        need_to_screenshot = await page.get_by_role(role="article").filter(has_text=self.search).all()
        if need_to_screenshot == []:
            return False
        for i in need_to_screenshot:
            global screenshot_bytes, link, date
            link = ""
            date = ""
            try:
                await i.scroll_into_view_if_needed()
                screenshot_bytes = await i.screenshot()
                link = await i.get_by_role("link").first.get_attribute("href")
                text = await i.inner_html()
                date = re.search('.*role="link" tabindex="0"><span>(?P<date>.*?)</span>.*', text).group("date")
            except Exception as e:
                logger.error("{}查找link失败:{}".format(self.search, e))
            self.results.append({"image_name": f"{time.time()}.png", "image":screenshot_bytes, "link":link, "date": date})
        logger.info(f"{self.search}: 任务全部完成")
        await page.close()

    async def start_screenshot(self):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(
                headless=True)
            now_time = time.time()
            with open(f"{BASE_DIR}/login_data/login_data_facebook.json", mode="r") as f:
                obj = json.load(f)
                expires = obj["cookies"][1]["expires"]
            # 如果过期时间小于现在时间，重新登录
            if now_time > expires:
                context = await self.login(await browser.new_context(viewport={"width": 1080, "height": 2920}), account=self.account)
            else:
                context = await browser.new_context(storage_state=f"{BASE_DIR}/login_data/login_data_facebook.json", viewport={"width": 1080, "height": 1920})
            #开始追踪
            await context.tracing.start(screenshots=True, snapshots=True, sources=True)
            await self.screenshot(context)
            #结束追踪
            await context.tracing.stop(path=f"{BASE_DIR}/trace/{self.orderId+'+'+time.strftime('%m月%d日%H时%M分')}.zip")
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




