# import asyncio
#
# from playwright.async_api import async_playwright
#
# cookies = [{"name": "sb", "value": "gYSaZJGa5P_zMhcWHk4GUfpj", "domain": ".facebook.com", "path": "/", "expires": 1722408070.028656, "httpOnly": True, "secure": True, "sameSite": "None"}, {"name": "wd", "value": "1280x720", "domain": ".facebook.com", "path": "/", "expires": 1688452867, "httpOnly": False, "secure": True, "sameSite": "Lax"}, {"name": "dpr", "value": "1.0000000298023224", "domain": ".facebook.com", "path": "/", "expires": 1688452867, "httpOnly": False, "secure": True, "sameSite": "None"}, {"name": "datr", "value": "gYSaZCU5QMt4opmNfSNfTPCl", "domain": ".facebook.com", "path": "/", "expires": 1722408070.02857, "httpOnly": True, "secure": True, "sameSite": "None"}, {"name": "c_user", "value": "100092873971824", "domain": ".facebook.com", "path": "/", "expires": 1719384068.028677, "httpOnly": False, "secure": True, "sameSite": "None"}, {"name": "xs", "value": "1%3ANlueDECTtwBK4w%3A2%3A1687848069%3A-1%3A2997", "domain": ".facebook.com", "path": "/", "expires": 1719384068.028695, "httpOnly": True, "secure": True, "sameSite": "None"}, {"name": "fr", "value": "0cmh5PTm5kVsnJaS1.AWWc0NrCRMTD7lD7Lq5mOCrW1EY.BkmoSB.JE.AAA.0.0.BkmoSH.AWXli_EIKVQ", "domain": ".facebook.com", "path": "/", "expires": 1695624069.47569, "httpOnly": True, "secure": True, "sameSite": "None"}]
# #"origins": [{"origin": "https://www.facebook.com", "localStorage": [{"name": "mutex_falco_queue_log^$100092873971824^#100092873971824^#^#hmac.AR3aRoq6LZDBE1SPWqT-wbLqwkh5mE37RMbC1eM-Y9sY9qxh^$", "value": "nt9cal:1687848076608"}, {"name": "Session", "value": "yt3u2y:1687848110530"}, {"name": "mutex_falco_queue_critical^$100092873971824^#100092873971824^#^#hmac.AR3aRoq6LZDBE1SPWqT-wbLqwkh5mE37RMbC1eM-Y9sY9qxh^$", "value": "nt9cal:1687848076608"}, {"name": "hb_timestamp", "value": "1687848067002"}, {"name": "signal_flush_timestamp", "value": "1687848067072"}, {"name": "mutex_falco_queue_immediately^$100092873971824^#100092873971824^#^#hmac.AR3aRoq6LZDBE1SPWqT-wbLqwkh5mE37RMbC1eM-Y9sY9qxh^$", "value": "nt9cal:1687848076608"}]}]
#
# async def run():
#     async with async_playwright() as playwright:
#         chromium = playwright.chromium  # or "firefox" or "webkit".
#         browser = await chromium.launch(
#             headless=False,
#             proxy={"server": "http://127.0.0.1:19180"})
#         context = await browser.new_context()
#         await context.add_cookies(cookies)
#         page = await context.new_page()
#         await page.goto("https://www.facebook.com")
#         await page.wait_for_timeout(10000)
#
# asyncio.run(run())
import re
import time

print(time.strftime('%Y年%m月%d日%H时:%M分:%S秒'))