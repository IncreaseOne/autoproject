import datetime
import re
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

list_files = os.listdir(path=r"F:\AutoTestCode\log")

for i in list_files:
    re_date = re.search("(?P<date>[\d|-]*).log", i)
    if re_date != None:
        date = re_date.group("date")
        timestamp = time.mktime(time.strptime(date, "%Y-%m-%d"))
        if time.time() - timestamp > 24*3600*10:
            os.remove(os.path.join("F:\AutoTestCode\log", i))
            print("删除成功"+os.path.join("F:\AutoTestCode\log", i))







