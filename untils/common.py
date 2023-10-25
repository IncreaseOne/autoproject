# -*- coding: utf-8 -*-
# author：王勇
import asyncio
import logging
import random
import threading
import time

logger = logging.getLogger(__name__)


# 将失败重跑的机制写成装饰器


class Decorator:


    # 异步函数重跑
    @staticmethod
    def run_failure(times=2):
        def start(case):
            async def inner(*args, **kwargs):
                nonlocal times
                try:
                    result = await case(*args, **kwargs)
                    return result
                except Exception as e:
                    logger.error("{}执行失败:{}".format(case.__name__, e))
                    if times > 0:
                        times -= 1
                        logger.error("开始重跑，剩余次数: {}".format(times))
                        wait_random = random.randint(3, 5)
                        logger.info("等待随机数:{}秒".format(wait_random))
                        await asyncio.sleep(wait_random)
                        return await inner(*args, **kwargs)
                    else:
                        logger.error("超过失败次数, 不再重跑: {}".format(e))
                        return True

            return inner

        return start



