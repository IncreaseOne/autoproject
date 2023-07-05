import os
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
        results = asyncio.run(screen_shot.run())
        if not results:
            return JsonResponse({"code": 400, "message": "折扣码无效"})
        return JsonResponse({"code": 200, "message":"成功", "data": [i for i in results]}, json_dumps_params={"ensure_ascii": False})



    def get(self, request):
        import asyncio

        from playwright.async_api import async_playwright
        from playwright.sync_api import sync_playwright

        def run():
            os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
            playwright = sync_playwright().start()
            chromium = playwright.chromium  # or "firefox" or "webkit".
            browser = chromium.launch(
                headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://www.baidu.com")
            browser.close()

        run()
        return JsonResponse({"code": 200})