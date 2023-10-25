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
    throttle_classes = ()
    q = Queue()
    p1 = None


    def match_execute_time(self, execute_time)-> list:
        upload_pictures = []
        def get_timestamp(obj:dict) -> None:
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
                obj["date"] = time.mktime(time.strptime(date, "%Y年%m月%d日")) + 24 * 3600 #加一天的时间
            elif obj.get("date").find("年") != -1:
                obj["date"] = time.mktime(time.strptime(obj.get("date"), "%Y年%m月%d日"))
            else:
                obj["date"] = now
        for result in self.data:
            global flag
            flag = 0
            if result.get("info") != None and isinstance(result, (dict)):
                for info in result.get("info"):
                    get_timestamp(info)
                    if info.get("date") >= execute_time:
                       link = S3().upload_single_file(info.get("image"), info.get("image_name"))
                       upload_pictures.append({"group_id": result.get("group_id"), "link": link, "timestamp": info.get("date")})
                       flag = 1
                       break;
                if not flag:
                    upload_pictures.append({"group_id": result.get("group_id"), "link": None, "timestamp": None})
                    flag = 0
        return upload_pictures


    def screen_shot_task(self, request_data):
        def callback(json_data: dict):
            for i in range(0, 3):
                response = requests.post(url=request_data.get("callback_link"), json=json_data).text
                logger.info("{}回调返回的数据{}".format(request_data.get("search"), response))
                json_res = json.loads(response)
                if json_res.get("code") == 200:
                    break;
        screen_shot = AutoScreenshot(search=request_data.get("search"),orderId=request_data.get("orderId"),groups=request_data.get("groups"))
        results = asyncio.run(screen_shot.start_screenshot())
        if not results:
            logger.info("{}任务执行失败".format(request_data.get("search")))
            callback({"code": 500, "message": "账号异常", "result_data": []})
            return
        self.execute_time = request_data.get("execute_time")
        self.data = [i for i in results]
        result_data = self.match_execute_time(request_data.get("execute_time"))
        result_data = [data for data in result_data if data != True]
        logger.info("{}返回的数据:{}".format(request_data.get("search"), result_data))
        callback({"code": 200, "message": "成功", "data": result_data})


    def start_thread(self):
        def deal_task():
            while True:
                if not Facebook.q.empty():
                    self.screen_shot_task(Facebook.q.get())
                else:
                    break

        if Facebook.p1 is None or Facebook.p1.is_alive() == False:
            Facebook.p1 = threading.Thread(target=deal_task)
            Facebook.p1.daemon = True
            Facebook.p1.start()





    def post(self, request):
        logger.info("自动截图请求参数{}".format(request.data))
        groups = request.data.get("groups")
        search = request.data.get("search")
        callback_link = request.data.get("callback_link")
        execute_time = request.data.get("execute_time")
        if not search or not groups or not callback_link or not execute_time:
            return JsonResponse({"code": 400, "message": "参数传递异常"}, json_dumps_params={"ensure_ascii": False})

        # 对link先处理一遍
        for i in range(0, len(groups)):
            if groups[i].get("group_link").find("?") != -1:
                args = re.search(".*(?P<args>\?.*)", groups[i].get("group_link")).group("args")
                groups[i]["group_link"] = groups[i].get("group_link").replace(args, "")
            groups[i]["group_link"] = groups[i].get("group_link").removesuffix("/") + f"/search?q={search}&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9In0%3D"

        Facebook.q.put(request.data)
        logger.info("当前剩余任务{}".format(Facebook.q.qsize()))
        self.start_thread()
        return JsonResponse({"code": 200, "message": "成功", "tasks": Facebook.q.qsize()})



    def get(self, request):
        screen_shot = AutoScreenshot()
        asyncio.run(screen_shot.start_login())
        return JsonResponse({"code": 200, "message": "登录成功"})


    def throttled(self, request, wait):
        raise throttle_exception(message="同一个订单不能重复请求", code=429, result_data=[])






