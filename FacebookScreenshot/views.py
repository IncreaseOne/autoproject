import datetime
import json
import os
import re
import threading
import time

import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
import logging
from FacebookScreenshot.facebookplaywright import AutoScreenshot
import asyncio

from untils.exception import throttle_exception

logger = logging.getLogger(__name__)
from multiprocessing import Queue, Process
from untils.awss3 import S3


from rest_framework.throttling import BaseThrottle

class FacebookThrottle(BaseThrottle):

    record = []


    def allow_request(self, request, view):
        orderId = request.data.get("orderId")
        now = int(time.time())
        if not self.record:
            self.record.append({"orderId":orderId, "time": now})
            return True
        else:
            if self.record[0].get("orderId") == orderId and now - self.record[0].get("time") < 120:
                return False
            else:
                self.record[0] = {"search":orderId, "time": now}
                return True




class Facebook(APIView):
    data = []
    S3 = S3()
    throttle_classes = (FacebookThrottle,)
    q = Queue()
    p1 = None


    def match_groupId(self, groupId):
        groupId = str(groupId)
        def get_timestmp(obj:dict) -> None:
            now = time.time()
            if isinstance(obj.get("date"), (float)):
                return
            elif obj.get("date").find("小时") != -1:
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
            elif obj.get("date").find("年") != -1:
                obj["date"] = time.mktime(time.strptime(obj.get("date"), "%Y年%m月%d日"))
            else:
                obj["date"] = now
        count = []
        for result in self.data:
            #判断是存在重复的折扣码
            get_timestmp(result)
            if str(result.get("link")).find(str(groupId)) != -1 and result.get("date") >= self.execute_time :
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
            for i in range(0, len(count)-1):
                if float(count[i].get("date")) < float(count[i+1].get("date")):
                    max = count[i+1]
            image_name = self.S3.upload_single_file(max.get("image"), max.get("image_name"))
            return {"link":image_name, "groupId":groupId, "timestamp":max.get("date")}


    def screen_shot_task(self, request_data):
        def callback(json_data: dict):
            for i in range(0, 3):
                response = requests.post(url=request_data.get("callback_link"), json=json_data).text
                logger.info("{}回调返回的数据{}".format(request_data.get("search"), response))
                json_res = json.loads(response)
                if json_res.get("code") == 200:
                    break;
        screen_shot = AutoScreenshot(search=request_data.get("search"), orderId=request_data.get("orderId"))
        results = asyncio.run(screen_shot.start_screenshot())
        if not results:
            logger.info("{}任务执行失败".format(request_data.get("search")))
            callback({"code": 400, "message": "请检查折扣码是否正常或者联系管理员", "result_data": []})
            return
        self.execute_time = request_data.get("execute_time")
        self.data = [i for i in results]
        result_data = map(self.match_groupId, request_data.get("groupIds"))
        result_data = [i for i in result_data if time.time() - i.get("timestamp") < 30 * 24 * 3600]
        request_data["result_data"] = result_data
        logger.info("{}返回的数据:{}".format(request_data.get("search"), result_data))
        callback(request_data)


    def start_thread(self):
        def deal_task():
            while True:
                if not Facebook.q.empty():
                    self.screen_shot_task(Facebook.q.get())
                else:
                    break

        if Facebook.p1 is None or Facebook.p1.is_alive() == False:
            Facebook.p1 = threading.Thread(target=deal_task)
            Facebook.p1.daemon =True
            Facebook.p1.start()





    def post(self, request):
        logger.info("自动截图请求参数{}".format(request.data))
        groupIds = request.data.get("groupIds")
        search = request.data.get("search")
        orderId = request.data.get("orderId")
        callback_link = request.data.get("callback_link")
        execute_time = request.data.get("execute_time")
        if not search or not groupIds or not orderId or not callback_link or not execute_time:
            return JsonResponse({"code": 400, "message": "参数传递异常"}, json_dumps_params={"ensure_ascii": False})
        Facebook.q.put(request.data)
        logger.info("当前剩余任务{}".format(Facebook.q.qsize()))
        self.start_thread()
        return JsonResponse({"code": 200, "message": "成功", "tasks": Facebook.q.qsize()})



    def get(self, request):
        screen_shot = AutoScreenshot()
        asyncio.run(screen_shot.start_login())
        return JsonResponse({"code": 200, "message": "登录成功"})


    def throttled(self, request, wait):
        raise throttle_exception(message="同一个订单不能重复请求", code=429)



