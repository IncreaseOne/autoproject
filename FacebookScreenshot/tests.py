import asyncio
import datetime
import re
import threading
import time
#
from functools import reduce

# from playwright.sync_api import Playwright, sync_playwright, expect
#
#
# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False, proxy={"server": "http://127.0.0.1:19180"})
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto(r"https://www.facebook.com/search/posts/?q={self.search}")
#     page.wait_for_timeout(100000)
#     element = page.locator("span", has_text=re.compile(".*已经到底啦~.*|.*找不到任何结果.*|.*加入或登录 Facebook.*|.*你的帐户已锁定.*"))
#     print(element.inner_html())
#     context.close()
#     browser.close()
#
# run(sync_playwright().start())








