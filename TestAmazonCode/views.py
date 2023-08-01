import asyncio
import os
import re
from threading import Thread

import requests
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
from rest_framework.views import APIView
import threading


class AmazonWebSite(APIView):



    def post(self, request):
        def test_code(request):
            data = json.loads(request.body.decode("utf-8")).get("data")
            callback_url = json.loads(request.body.decode("utf-8")).get("url")
            compile_amazon = re.compile('^.*?www\.amazon\.(?P<country>[a-zA-Z\.]*)/')

            def add_task(goodsUrl_and_code):
                group_country = re.search(compile_amazon, goodsUrl_and_code["goods_url"])
                if group_country:
                    country = group_country.group("country")
                    type = 1 if goodsUrl_and_code["goods_url"].find("promocode") == -1 else 2
                    goodsUrl_and_code["type"] = type
                    goodsUrl_and_code["country"] = country
                    return goodsUrl_and_code
                else:
                    goodsUrl_and_code["status"] = 2
                    return goodsUrl_and_code


            tasks = filter(add_task, data)
            amazonAutoTest = AmazonAutoTest(tasks=tasks)
            result = asyncio.run(amazonAutoTest.do_task())
            result = result if type(result) == str else [r for r in result]
            requests.post(json=result, url=callback_url)

        threading.Thread(target=test_code, args=(request,)).start()
        return JsonResponse({"code": 200, "message": "成功"})










