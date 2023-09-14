# -*- coding: utf-8 -*-
# author：王勇
import logging
import random
import threading
import time

logger = logging.getLogger(__name__)


#将失败重跑的机制写成装饰器


class decorator:

    @staticmethod
    def run_failure(times=3):
        def start(case):
            def inner(*args, **kwargs):
                nonlocal times
                try:
                    result = case(*args, **kwargs)
                    return result
                except Exception as e:
                    logger.error("{}执行失败:{}".format(case.__name__, e))
                    if times >= 0:
                        times -= 1
                        logger.error("开始重跑，剩余次数: {}".format(times))
                        return inner(*args, **kwargs)
                    else:
                        logger.error("超过失败次数, 不再重跑: {}".format(e))
            return inner
        return start




@decorator.run_failure(times=3)
def get(name, age):
    t = 8 / random.randint(0, 1)
    return t


