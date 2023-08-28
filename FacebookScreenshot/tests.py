import re

from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False, proxy={"server": "http://127.0.0.1:19180"})
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://rkf2ppgd6v.feishu.cn/sheets/shtcnsOoF4zcXIPOibma5F2Tx13")
#     with page.expect_download() as download_info:
#         content = page.locator("div").filter(has_text=re.compile(r"^弹性小狗项圈\.mp4单元格内容以文本形式存储$")).inner_html()
#     context.close()
#     browser.close()

#
# with sync_playwright() as playwright:
#     run(playwright)
