import os
import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
import logging
from FacebookScreenshot.facebookplaywright import AutoScreenshot
import asyncio
logger = logging.getLogger(__name__)

class Facebook(APIView):
    data = []
    result_data = {}

    def match_groupId(self, groupId):
        groupId = str(groupId)
        for i in Facebook.data:
            if i.get("link").find(groupId) != -1:
                return {groupId: i.get("image")}
        return {groupId: None}


    def post(self, request):
        code = request.data.get("code")
        groupIds = request.data.get("groupIds")
        if not code or not groupIds or code == "nocode" or code == "no code":
            return JsonResponse({"code": 400, "message": "参数传递异常"}, json_dumps_params={"ensure_ascii": False})
        screen_shot = AutoScreenshot(code=code)
        results = asyncio.run(screen_shot.start_screenshot())
        Facebook.data = [i for i in results]
        logger.info("{}任务返回的数据{}".format(code, Facebook.data))
        result_data = map(self.match_groupId, groupIds)
        result_data = {k:v for item in result_data for k,v in item.items()}
        logger.info("{}返回的数据{}".format(code, result_data))
        if not results:
            return JsonResponse({"code": 400, "message": "折扣码无效"})
        return JsonResponse({"code": 200, "message":"成功", "data": result_data}, json_dumps_params={"ensure_ascii": False})


