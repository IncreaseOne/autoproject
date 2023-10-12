# -*- coding: utf-8 -*-
# author：王勇
import time

def discard_time(timeStamp: int)-> int:
    timeArray = time.localtime(timeStamp)
    date = time.strftime("%Y-%m-%d", timeArray)
    date_time = time.strptime(date, "%Y-%m-%d")
    return int(time.mktime(date_time))


