import asyncio
import datetime
import re
import threading
import time
#
from functools import reduce

# from playwright import async_api
#
#
#
# async def test():
#     async with async_api.async_playwright() as playwright:
#         launch = await playwright.chromium.launch()
#         context = await launch.new_context()
#         page = await context.new_page()
#         await page.goto("https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%C3%C0%C5%AE%CD%BC%C6%AC&fr=ala&ala=1&alatpl=normal&pos=0&dyTabStr=MTEsMCwzLDQsMSw2LDUsMiw4LDcsOQ%3D%3D")
#         inner_html = await page.locator("html").inner_html()
#         print("<document>"+inner_html+"</document>")
#
#
# asyncio.run(test())








