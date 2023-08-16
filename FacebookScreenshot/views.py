import datetime
import os
import re
import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
import logging
from FacebookScreenshot.facebookplaywright import AutoScreenshot
import asyncio
logger = logging.getLogger(__name__)
from playwright import sync_api
from untils.awss3 import S3
class Facebook(APIView):
    data = []
    S3 = S3()

    def match_groupId(self, groupId):
        groupId = str(groupId)
        def get_timestmp(obj:dict) -> None:
            now = time.time()
            if isinstance(obj.get("date"), (float)):
                return
            if obj.get("date").find("小时") != -1:
                hours = re.search("(?P<hours>\d*)小时", obj.get("date")).group("hours")
                obj["date"] = now - int(hours) * 3600
            elif obj.get("date").find("天") != -1:
                days = re.search("(?P<days>\d*)天", obj.get("date")).group("days")
                obj["date"] = now - int(days) * 24 * 3600
            elif re.search("^\d*月\d*日", obj.get("date")) != None:
                current_year = datetime.datetime.now().year
                date = f"{current_year}年{obj.get('date')}"
                obj["date"] = time.mktime(time.strptime(date, "%Y年%m月%d日"))
            elif obj.get("date").find("年") != None:
                obj["date"] = time.mktime(time.strptime(i.get("date"), "%Y年%m月%d日"))
            else:
                obj["date"] = now
        count = []
        for result in self.data:
            #判断是存在在重复的折扣码
            if str(result.get("link")).find(str(groupId)) != -1:
                count.append(result)
        if len(count) == 0:
            return {"link":None, "groupId":groupId, "timestamp":time.time()}
        elif len(count) == 1:
            image_name = self.S3.upload_single_file(image=count[0].get("image"), file_name=count[0].get("image_name"))
            get_timestmp(count[0])
            return {"link":image_name, "groupId":groupId, "timestamp":count[0].get("date")}
        # 存在重复的折扣码截图, 取时间最早的
        else:
            max = count[0]
            for i in count:
                # 先转为时间戳
                get_timestmp(i)

            # 得到最大的时间戳
            for i in range(0, len(count)):
                if float(count[i].get("date")) < float(count[i+1].get("date")):
                    max = count[i+1]
            image_name = self.S3.upload_single_file(max.get("image"), max.get("image_name"))
            return {"link":image_name, "groupId":groupId, "timestamp":max.get("date")}










    def post(self, request):
        print(request.data)
        groupIds = request.data.get("groupIds")
        search = request.data.get("search")
        orderId = request.data.get("orderId")
        if not search or not groupIds or not orderId:
            return JsonResponse({"code": 400, "message": "参数传递异常"}, json_dumps_params={"ensure_ascii": False})
        screen_shot = AutoScreenshot(search=search, orderId=orderId)
        results = asyncio.run(screen_shot.start_screenshot())
        if not results:
            return JsonResponse({"code": 400, "message": "请检查折扣码是否正常然后联系管理员"}, json_dumps_params={"ensure_ascii": False})
        self.data = [i for i in results]
        result_data = map(self.match_groupId, groupIds)
        result_data = list(result_data)
        logger.info("{}返回的数据:{}".format(search, result_data))
        return JsonResponse({"code": 200, "message":"成功", "data": result_data}, json_dumps_params={"ensure_ascii": False})

    def get(self, request):
        screen_shot = AutoScreenshot()
        asyncio.run(screen_shot.start_login())
        return JsonResponse({"code": 200, "message": "登录成功"})


