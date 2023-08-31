import datetime
import re
import threading
import time
#
from functools import reduce

from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False, proxy={"server": "http://127.0.0.1:19180"})
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto(r"https://www.baidu.com")
#     page.mouse.click(564,603, button="left")
#     print(page.e)
#     page.wait_for_timeout(100000)
#     context.close()
#     browser.close()
#
# run(sync_playwright().start())



import os

def test(id, name):
    print(id, name)


thread1 = threading.Thread(target=test, kwargs={"id":"123", "name": "李四"}).start()







