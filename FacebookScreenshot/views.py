import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from FacebookScreenshot.facebookplaywright import AutoScreenshot
import asyncio

class Facebook(APIView):


    def post(self, request):
        code = request.data.get("code")
        if not code:
            return JsonResponse({"code": 400, "message": "参数传递异常"}, json_dumps_params={"ensure_ascii": False})
        screen_shot = AutoScreenshot(code=code)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(screen_shot.run())
        if not results:
            return JsonResponse({"code": 400, "message": "折扣码无效"})
        return JsonResponse({"code": 200, "message":"成功", "data": [i for i in results]}, json_dumps_params={"ensure_ascii": False})


