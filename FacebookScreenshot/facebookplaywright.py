# -*- coding: utf-8 -*-
# author：王勇
import asyncio
import base64
import json
import os
import queue
import re
import time
import logging
import random

from django.core.mail import send_mail
from playwright.async_api import async_playwright, expect
from apscheduler.schedulers.background import BackgroundScheduler
from AutoTestCode.settings import BASE_DIR
from untils.common import Decorator
logger = logging.getLogger(__name__)





class AutoScreenshot():
    main_page = "https://www.facebook.com"
    proxy = {"server": "http://127.0.0.1:19180"}
    account = {"username": "czh18030315579@gmail.com", "password": "chen.1314520"}

    def __init__(self, search=None, orderId=None, groups: []=None):
        self.orderId = orderId
        self.results = []
        self.q = queue.Queue()
        self.search = search
        for i in groups:
            self.q.put(i)

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

    @Decorator.run_failure(times=2)
    async def screenshot(self, context, group):
        info = [] # 每一个群组的截图相关信息
        page = await context.new_page()
        # await page.goto(f'https://www.facebook.com/search/posts/?q={self.search}&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D')
        # logging.info(f"{self.search}: 页面渲染完成")
        # if await page.get_by_text("展开").count() > 0:
        #     expands = await page.get_by_text("展开").all()
        #     for i in expands:
        #         try:
        #             await i.click()
        #         except:
        #             pass
        # move_wheel_before = time.time()
        # while await page.locator("span", has_text=re.compile(".*已经到底啦~.*|.*找不到任何结果.*|.*加入或登录 Facebook.*|.*你的帐户已锁定.*")).is_visible(timeout=3000) is False:
        #     await page.mouse.wheel(0, 500)
        #     if await page.get_by_text("展开").count() > 0:
        #         expands = await page.get_by_text("展开").all()
        #         for i in expands:
        #             try:
        #                 await i.click(timeout=3000)
        #             except:
        #                 pass
        #     elif time.time() - move_wheel_before > 600:
        #         return False
        #
        # logging.info(f"{self.search}: 页面展开到底部")
        # await page.mouse.wheel(0, 0)
        # await page.mouse.move(0,0)
        # logger.info(f"{self.search}: 页面回到顶部")
        # need_to_screenshot = await page.get_by_role(role="article").filter(has_text=self.search).all()
        # if need_to_screenshot == []:
        #     return False
        # for i in need_to_screenshot:
        #     global screenshot_bytes, link, date
        #     link = ""
        #     date = ""
        #     try:
        #         await i.scroll_into_view_if_needed()
        #         screenshot_bytes = await i.screenshot()
        #         link = await i.get_by_role("link").first.get_attribute("href")
        #         text = await i.inner_html()
        #         date = re.search('.*role="link" tabindex="0"><span>(?P<date>.*?)</span>.*', text).group("date")
        #     except Exception as e:
        #         logger.error("{}查找link失败:{}".format(self.search, e))
        #     now_time = time.time()
        #     image_name = f"{now_time}.png"
        #     logger.info("截图成功{}".format(image_name))
        #     self.results.append({"image_name": image_name, "image":screenshot_bytes, "link":link, "date": date})
        # logger.info(f"{self.search}: 任务全部完成")
        # await page.close()

        group_link = group.get("group_link")
        await page.goto(group_link, timeout=50000)
        logging.info(f"{group_link}: 页面渲染完成")
        if await page.get_by_text("展开").count() > 0:
            expands = await page.get_by_text("展开").all()
            for i in expands:
                try:
                    await i.click()
                except:
                    pass
        move_wheel_before = time.time()
        while await page.locator("span", has_text=re.compile(".*已经到底啦~.*|.*在这个小组中找不到任何结果.*|内容暂时无法显示")).is_visible(timeout=3000) is False:
            await page.mouse.wheel(0, 500)
            if await page.get_by_text("展开").count() > 0:
                expands = await page.get_by_text("展开").all()
                for j in expands:
                    try:
                        await j.click(timeout=3000)
                    except:
                        pass
            if time.time() - move_wheel_before > 300:
                # 账号出现异常
                logger.info("facebook账号出现异常")
                return False
        logging.info(f"{group_link}: 页面展开到底部")
        await page.mouse.wheel(0, 0)
        logger.info(f"{group_link}: 页面回到顶部")
        need_to_screenshot = await page.get_by_role(role="article").filter(has_text=self.search).all()
        if need_to_screenshot == []:
            # 该网红未发帖
            self.results.append(group)
            return True

        for i in need_to_screenshot:
            global screenshot_bytes
            global link
            global date
            try:
                await i.scroll_into_view_if_needed()
                screenshot_bytes = await i.screenshot()
                link = await i.get_by_role("link").first.get_attribute("href")
                text = await i.inner_html()
                date = re.search('.*role="link" tabindex="0"><span>(?P<date>.*?)</span>.*', text).group("date")
            except Exception as e:
                logger.error("{}查找link失败:{}".format(self.search, e))
            now_time = time.time()
            image_name = f"{now_time}.png"
            logger.info("截图成功{}".format(image_name))
            info.append({"image_name": image_name, "image":screenshot_bytes, "link":link, "date": date})
        info.reverse()
        group["info"] = info
        self.results.append(group)
        await page.close()
        return True




    async def start_screenshot(self):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(
                headless=True
            )
            now_time = time.time()
            with open(f"{BASE_DIR}/login_data/login_data_facebook.json", mode="r") as f:
                obj = json.load(f)
                expires = obj["cookies"][1]["expires"]
            # 如果过期时间小于现在时间，重新登录
            if now_time > expires:
                context = await self.login(await browser.new_context(viewport={"width": 1080, "height": 1920}), account=self.account)
            else:
                context = await browser.new_context(storage_state=f"{BASE_DIR}/login_data/login_data_facebook.json", viewport={"width": 1080, "height": 1920})
            #开始追踪
            await context.tracing.start(screenshots=True, snapshots=True, sources=True)
            while True:
                if self.q.empty():
                    break;
                else:
                    tasks = []
                    if self.q.qsize() >= 1:
                        for i in range(0, 1):
                            tasks.append(self.screenshot(context, self.q.get()))
                    else:
                        for i in range(0, self.q.qsize()):
                            tasks.append(self.screenshot(context, self.q.get()))
                    every_results = await asyncio.gather(*tasks)
                    await asyncio.sleep(random.randint(3, 6))
                    if False in every_results:
                        send_mail(f"{self.account.get('username')}账号状态异常", message="", from_email="279761649@qq.com", recipient_list=["279761649@qq.com"])
                        return False
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




