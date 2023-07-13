import os
import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from FacebookScreenshot.facebookplaywright import AutoScreenshot
import asyncio


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
        result_data = map(self.match_groupId, groupIds)
        result_data = {k:v for item in result_data for k,v in item.items()}
        if not results:
            return JsonResponse({"code": 400, "message": "折扣码无效"})
        return JsonResponse({"code": 200, "message":"成功", "data": result_data}, json_dumps_params={"ensure_ascii": False})


