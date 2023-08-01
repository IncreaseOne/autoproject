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
from playwright import sync_api
from untils.awss3 import S3
class Facebook(APIView):
    groupIds = []
    S3 = S3()

    def match_groupId(self, result_data_Item):
        link = result_data_Item.get("link")
        image_name = result_data_Item.get("image_name")
        image = result_data_Item.get("image")
        for groupId in self.groupIds:
            if link != None and link.find(str(groupId)) != -1:
                url_name = self.S3.upload_single_file(image, file_name=image_name)
                return {groupId: url_name}




    def post(self, request):
        code = request.data.get("code")
        self.groupIds = request.data.get("groupIds")
        if not code or not self.groupIds or code == "nocode" or code == "no code":
            return JsonResponse({"code": 400, "message": "参数传递异常"}, json_dumps_params={"ensure_ascii": False})
        screen_shot = AutoScreenshot(code=code)
        results = asyncio.run(screen_shot.start_screenshot())
        if not results:
            return JsonResponse({"code": 400, "message": "请检查折扣码是否正常然后联系管理员"}, json_dumps_params={"ensure_ascii": False})
        data = [i for i in results]
        result_data = map(self.match_groupId, data)
        result_data = { k:v for i in list(result_data) if i != None for k,v in i.items() }
        logger.info("{}返回的数据:{}".format(code, result_data))
        return JsonResponse({"code": 200, "message":"成功", "data": result_data}, json_dumps_params={"ensure_ascii": False})

    def get(self, request):
        screen_shot = AutoScreenshot(code=None)
        asyncio.run(screen_shot.start_login())
        return JsonResponse({"code": 200, "message": "登录成功"})


