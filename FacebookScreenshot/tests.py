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
groupIds = ["dsa", "dasd", "dsad", "dsa"]
def match_groupId(result_data_Item):
    link = result_data_Item.get("link")
    image_name = result_data_Item.get("image_name")
    image = result_data_Item.get("image")
    for groupId in groupIds:
        if link != None and link.find(groupId) != -1:
            return {groupId: "hello"}

result_data = list(map(match_groupId, [{"link": None, "image_name":12, "image": 12}, {"link": "dsa", "image_name":12, "image": 12}]))

result_data = { k:v for i in list(result_data) if i != None for k,v in i.items() }
print(result_data)






