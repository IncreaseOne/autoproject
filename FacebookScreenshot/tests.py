# from playwright.sync_api import sync_playwright
#
#
# def run():
#     playwright = sync_playwright().start()
#     chromium = playwright.chromium  # or "firefox" or "webkit".
#     browser = chromium.launch(
#         proxy={'server': 'http://127.0.0.1:19180'},
#         headless=True)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto(r"https://www.facebook.com/groups/1673433336025800/about")
#     e = page.locator("div[aria-label='Accessible login button']")
#     print(e)
#     browser.close()
#
#
# run()

def match_groupId(groupId):
    groupId = str(groupId)
    for i in [{"link": "href/dsadsa/dsad", "image": "htdadua://www.baidu.com"}]:
        if i.get("link").find(groupId) != -1:
            return {groupId:i.get("image")}
    return {groupId: None}

r = map(match_groupId, ["dsadsa"])
print(list(r))