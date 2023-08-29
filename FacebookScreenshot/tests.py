import datetime
import re
import time
#
# from playwright.sync_api import Playwright, sync_playwright, expect
#
#
# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False, proxy={"server": "http://127.0.0.1:19180"})
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto(r"D:\vue_test\正则学习\匹配文本.html")
#     need_to_screenshot = page.get_by_role(role="article").filter(has_text="PreXquisite,Men's Short Sleeve T-Shirt,Mens T-Shirt, Oversized Men's Crewneck T-Shirt, Men's Undershirt").first
#     print(need_to_screenshot.inner_html())
#     context.close()
#     browser.close()
#
# run(sync_playwright().start())
print("20分钟".find("年") != None)




