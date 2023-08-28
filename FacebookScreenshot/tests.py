import datetime
import re
import time

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

data = [{"link": "127.0.0.1:/861/img", "date": "2月8日", "image_name": "test1", "image": "test1"},{"link": "127.0.0.1:/861/img2", "date": "3天", "image_name": "test2", "image": "test2"}]

def match_groupId(groupId):
    groupId = str(groupId)

    def get_timestmp(obj: dict) -> None:
        now = time.time()
        if isinstance(obj.get("date"), (float)):
            return
        if obj.get("date").find("小时") != -1:
            hours = re.search("(?P<hours>\d*)小时", obj.get("date")).group("hours")
            obj["date"] = now - int(hours) * 3600
        elif obj.get("date").find("天") != -1:
            days = re.search("(?P<days>\d*)天", obj.get("date")).group("days")
            obj["date"] = now - int(days) * 24 * 3600
        elif re.search("\d*月\d*日", obj.get("date")) != None:
            date_time = re.search("(?P<date>\d*月\d*日)", obj.get('date')).group("date")
            current_year = datetime.datetime.now().year
            date = f"{current_year}年{date_time}"
            obj["date"] = time.mktime(time.strptime(date, "%Y年%m月%d日"))
        elif obj.get("date").find("年") != None:
            obj["date"] = time.mktime(time.strptime(i.get("date"), "%Y年%m月%d日"))
        else:
            obj["date"] = now

    count = []
    for result in data:
        # 判断是存在在重复的折扣码
        if str(result.get("link")).find(str(groupId)) != -1:
            count.append(result)
    if len(count) == 0:
        return {"link": None, "groupId": groupId, "timestamp": time.time()}
    elif len(count) == 1:
        get_timestmp(count[0])
        return {"link": None, "groupId": groupId, "timestamp": count[0].get("date")}
    # 存在重复的折扣码截图, 取时间最早的
    else:
        max = count[0]
        for i in count:
            # 先转为时间戳
            get_timestmp(i)
        # 得到最大的时间戳
        for i in range(0, len(count) - 1):
            print("图片重复：" + count[i].get("link"))
            print(count[i + 1].get("link"))
            if float(count[i].get("date")) < float(count[i + 1].get("date")):
                max = count[i + 1]
        return {"link": max.get("link"), "groupId": groupId, "timestamp": max.get("date")}


test = map(match_groupId, ["861"])

print(list(test))
