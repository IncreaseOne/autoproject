import asyncio
import os
import re
from threading import Thread

from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .models import codeForm
from selenium import webdriver
import logging
logger = logging.getLogger(__name__)
from .AmzonSelenium import AmazonAutoTest
from multiprocessing import Queue, Manager
from multiprocessing import Process, Pool
from concurrent.futures import ProcessPoolExecutor
import json
from collections import deque
from rest_framework.views import APIView
drivers = deque()
def testCode(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))["data"]
        compile_amazon = re.compile(pattern="^.*?www\.amazon\.([a-zA-Z\.]*)/")
        def add_task(goodsUrl_and_code):
            country = re.findall(compile_amazon, goodsUrl_and_code["goods_url"])[0]
            type = 1 if goodsUrl_and_code["goods_url"].find("promocode") == -1 else 2
            goodsUrl_and_code["type"] = type
            goodsUrl_and_code["country"] = country
            return goodsUrl_and_code
        tasks = map(add_task, data)
        amazonAutoTest = AmazonAutoTest(tasks=tasks)
        result = asyncio.run(amazonAutoTest.do_task())
        result = result if type(result) == str else [r for r in result]
        return JsonResponse({"code": 200, "data": result})
    else:
        return JsonResponse({"code": 400, "message": "请求方式错误"})









