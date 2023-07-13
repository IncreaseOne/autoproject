# -*- coding: utf-8 -*-
# author：王勇
import asyncio
import random

from playwright.async_api import async_playwright
from playwright.async_api import expect
import logging
from AutoTestCode.settings import AMAZON_ACCOUNT
from queue import Queue

logger = logging.getLogger(__name__)


class AmazonAutoTest():
    '''
        :params cookies 做为浏览器的身份标识
        :params country_index 国家的索引，需要切换城市的时候使用
        :params tasks 线程池的任务列表
        :params driver 驱动对象
        :params type
    '''
    proxy = {"server": "http://127.0.0.1:19180"}
    browserLaunchOptionDict = {"headless": False, "proxy": {"server": proxy}}
    pages = []
    status_with_url = []

    def __init__(self, tasks):
        self.q = Queue()
        self.pageCookie = None
        self.results = []
        self.username = AMAZON_ACCOUNT["username"]
        self.password = AMAZON_ACCOUNT["password"]
        for task in tasks:
            self.q.put(task)

    async def loginAmazon(self, email, password, page, failed_time=5, country="com"):
        main_page_url = f"https://www.amazon.{country}/?language=US"
        try:
            await page.goto(main_page_url, timeout=0)
            if await page.locator(".nav-bb-right > a").first.is_visible():
                logger.info("进入非正常页面，正在处理")
                await page.locator(".nav-bb-right > a").first.click()
            logger.info("成功进入amazon主页")
            await page.click("span#nav-link-accountList-nav-line-1")
            await page.fill("#ap_email", email)
            await page.click("#continue")
            await page.fill("#ap_password", password)
            await page.click("#signInSubmit")
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_timeout(3000)
            if await page.locator("#ap_password").is_visible():
                logger.info("被页面检测， 输入密码， 等待用户输入验证码并确定")
                await page.fill("#ap_password", password)
            await page.reload()
            await page.wait_for_selector("#nav-logo", timeout=3000000)
            logger.info("成功登录")
            self.pages.append({"page": page, "country": country})
            return page
        except Exception as e:
            logger.error("登录失败:{}".format(e))
            if failed_time > 0:
                failed_time -= 1
                logger.info("重新登录, 剩余登录次数:{}".format(failed_time))
                await page.close()
                return await self.loginAmazon(email, password, await self.context.new_page(), failed_time=failed_time, country=country)
            else:
                logger.info("登录失败超过限制，不再重新登录")
                await page.close()

    '''
        @需要参数 email password country code type
    '''
    async def goods_detail(self, page, amazon_info: dict):
        await page.wait_for_timeout(random.randint(1, 5) * 1000)
        await page.goto(amazon_info["goods_url"], timeout=50000)
        if amazon_info["type"] == 2:
            logger.info("检测类型为社交类型")
            await page.locator('#grid > .grid > div').first.click()
            await page.wait_for_load_state("domcontentloaded")
        # 选择全部的规格
        selects = await page.get_by_role("combobox").all()
        for select in selects:
            await select.select_option(index=1)
        await page.wait_for_load_state("load")
        # 将商品加入购物车
        if await page.locator("#dealsx_atc_btn").is_visible(timeout=10000):
            await page.click("#dealsx_atc_btn")
        else:
            await expect(page.locator("#contextualIngressPtPin").first).to_be_visible()
            await page.click("#add-to-cart-button")
            await page.wait_for_load_state("domcontentloaded")
            try:
                await page.wait_for_load_state("networkidle")
            except:
                pass
        # 检查是否有弹框页面
        # 类型一
        if await page.locator("#turbo-checkout-place-order-button").count() > 0:
            await page.locator("#turbo-checkout-place-order-button").click()
            await page.wait_for_load_state("domcontentloaded")
        # 检查是否需要再次选择规格
        # 类型二
        if await page.locator("#attachSiNoCoverage").count() > 0:
            await page.locator("#attachSiNoCoverage").click()
            await page.wait_for_load_state("domcontentloaded")
        # 类型三右侧栏
        if await page.locator("#attach-accessory-pane #attach-sidesheet-checkout-button").count() > 0:
            await expect(
                page.locator("#attach-accessory-pane  #attach-sidesheet-checkout-button")).to_be_visible()
            await page.locator("#attach-accessory-pane  #attach-sidesheet-checkout-button").click()
            await page.wait_for_load_state("domcontentloaded")
        return page

    async def go_to_cart(self, page):
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(5000)
        if await page.locator("#sc-buy-box-ptc-button").count() > 0:
            await page.click("#sc-buy-box-ptc-button")
        return page

    async def choice_address(self, page):
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(5000)
        # 确认地址
        if await page.locator("#shipToThisAddressButton > span").count() > 0:
            await page.locator("#shipToThisAddressButton > span").click()
        return page

    async def order_detail(self, page, amazon_info: dict):
        # 如果直接下单的订单需要先取消
        if await page.locator("#prime-interstitial-nothanks-button").count() > 0:
            await page.click("#prime-interstitial-nothanks-button")
        # 下单后可能需要处理弹框
        if await page.locator("#action-buttons .prime-no-button").count() > 0:
            await page.locator("#action-buttons .prime-no-button").click()
        await page.wait_for_timeout(10000)
        # *** 需要将折扣码的具体测试优化为一个函数
        if await page.locator("#spc-gcpromoinput").count() > 0:
            code_content_before_enter_apply = await page.locator("#spc-order-summary td").all_inner_texts()
            code_content_before_enter_apply = "".join([x.replace("\n", "").replace(" ", "") for x in code_content_before_enter_apply])
            if code_content_before_enter_apply.find(amazon_info["code"]) != -1:
                logger.info("{}提前检测到折扣码".format(amazon_info["goods_url"]))
                amazon_info["status"] = 1
                amazon_info["code_content"] = code_content_before_enter_apply
                await page.close()
                return amazon_info
            # 等待apply可点击
            await page.locator("#spc-gcpromoinput").type(
                amazon_info["code"])
            await page.wait_for_timeout(5000)
            await page.click("#gcApplyButtonId")
            # 等待折扣码
            await page.wait_for_timeout(3000)
            await page.locator("#spc-gcpromoinput").click()
            await page.wait_for_timeout(5000)
            # 只需要判断 Promotion Applied字段或者折扣码(修改为判断折扣码以及successfully)
            result_content = ""
            result_contents = await page.locator(".a-alert-content > p").all()
            for result in result_contents:
                if await result.is_visible():
                    text = await result.inner_text()
                    result_content += text.replace("\n", "").replace(" ", "")
            logger.info("{}获取结果{}".format(amazon_info["goods_url"], result_content))
            # 第三层判断，点击apply之后，获取右侧折扣码进行对比
            code_content_after_enter_apply = await page.locator(
                "#spc-order-summary td").all_inner_texts()
            code_content_after_enter_apply = "".join(
                [x.replace("\n", "").replace(" ", "") for x in code_content_after_enter_apply])
            logger.info("%s开始验证折扣码" % amazon_info["goods_url"])
            if result_content.find("successfully") != -1 or code_content_after_enter_apply.find(amazon_info["code"]) != -1:
                amazon_info["status"] = 1
            else:
                amazon_info["status"] = 0
            amazon_info["result_content"] = result_content
            amazon_info["code_content_before_enter_apply"] = code_content_before_enter_apply
            amazon_info["code_content_after_enter_apply"] = code_content_after_enter_apply
        # 普通类型商品的分类二
        else:
            code_content_before_enter_apply = await page.locator("#spc-order-summary td").all_inner_texts()
            code_content_before_enter_apply = "".join([x.replace("\n", "").replace(" ", "") for x in code_content_before_enter_apply])
            if code_content_before_enter_apply.find(amazon_info["code"]) != -1:
                logger.info("{}提前检测到折扣码".format(amazon_info["goods_url"]))
                amazon_info["status"] = 1
                amazon_info["code_content"] = code_content_before_enter_apply
                await page.close()
                return amazon_info
            # 等待apply可点击
            await page.locator(".pmts-claim-code").type(amazon_info["code"])
            await page.wait_for_timeout(5000)
            await page.click(".pmts-claim-code-apply-button")
            # 等待折扣码
            await page.wait_for_timeout(3000)
            await page.locator(".pmts-claim-code").click()
            await page.wait_for_timeout(5000)
            # 判断的两种方式第一种是successfully 第二种判断是否有折扣码展示
            result_contents = await page.locator(".a-alert-content > p").all()
            result_content = ""
            for result in result_contents:
                text = await result.inner_text()
                result_content += text.replace("\n", "").replace(" ", "")
            logger.info("{}获取结果{}".format(amazon_info["goods_url"] ,result_content))
            # 第三层判断，点击apply之后，获取右侧折扣码进行对比
            code_content_after_enter_apply = await page.locator(
                "#spc-order-summary td").all_inner_texts()
            code_content_after_enter_apply = "".join(
                [x.replace("\n", "").replace(" ", "") for x in code_content_after_enter_apply])
            logger.info("%s开始验证折扣码" % amazon_info["goods_url"])
            if result_content.find("successfully") != -1 or code_content_before_enter_apply.find(amazon_info["code"]) != -1 or code_content_after_enter_apply.find(amazon_info["code"]) != -1:
                amazon_info["status"] = 1
            else:
                amazon_info["status"] = 0
            amazon_info["result_content"] = result_content
            amazon_info["code_content_before_enter_apply"] = code_content_before_enter_apply
            amazon_info["code_content_after_enter_apply"] = code_content_after_enter_apply
        self.status_with_url.append({"url": amazon_info["goods_url"], "status": amazon_info["status"]})
        return amazon_info

    async def delete_tasks_goods(self):
        try:
            logger.info("开始删除购物车每次执行任务的内容")
            await self.page.wait_for_load_state("domcontentloaded")
            await self.page.click("#nav-cart")
            await self.page.wait_for_load_state("domcontentloaded")
            goods = await self.page.locator(".sc-action-delete > .a-declarative > input").all()
            if len(goods) < 1:
                return
            for good in goods:
                await good.click(timeout=5000)
                await self.page.wait_for_load_state("domcontentloaded")
        except Exception as e:
            logger.info("删除购物车失败{}".format(e))

    async def delete_all_goods(self, failed_time=1):
        try:
            logger.info("开始删除购物车所有内容")
            await self.page.wait_for_load_state("domcontentloaded")
            await self.page.click("#nav-cart")
            await self.page.wait_for_load_state("domcontentloaded")
            goods = await self.page.locator(".sc-action-delete > .a-declarative > input").all()
            if len(goods) < 1:
                logger.info("购物车全部删除完毕")
                return
            for good in goods:
                await good.click(timeout=5000)
                await self.page.wait_for_load_state("domcontentloaded")
        except Exception as e:
            if failed_time > 0:
                failed_time -= failed_time
                logger.info("重新删除购物车{}".format(e))
                await self.delete_all_goods(failed_time=failed_time)
            else:
                logger.info("购物车删除超过失败次数{}".format(e))

    async def start_test_code(self, page, amazon_info: dict, failed_time=2):
        # 判断当前的url是否被测试，如果被测试过，则直接取出
        for item in self.status_with_url:
            if amazon_info["code"] == item["url"]:
                amazon_info["status"] = item["status"]
                await page.close()
                return amazon_info
        try:
            flag = False
            for p in self.pages:
                if p["country"] == amazon_info["country"]:
                    flag = True
            if flag is False:
                page = await self.loginAmazon(email=self.username, password=self.password, page=page,
                                              country=amazon_info["country"])
            # 开始测试
            page = await self.goods_detail(page, amazon_info)
            page = await self.go_to_cart(page)
            page = await self.choice_address(page)
            result = await self.order_detail(page, amazon_info)
            await page.close()
            return result
        except Exception as e:
            if failed_time > 0:
                failed_time -= 1
                logger.error("{}折扣码测试失败, 重新测试, 报错: {}".format(amazon_info["goods_url"], e))
                if page:
                    await page.close()
                return await self.start_test_code(await self.context.new_page(), amazon_info, failed_time=failed_time)
            else:
                logger.error("{}超过失败次数,不再重跑：{}".format(amazon_info["goods_url"], e))
                amazon_info["status"] = 2
                self.status_with_url.append({"url": amazon_info["goods_url"], "status": amazon_info["status"]})
                if page:
                    await page.close()
                return amazon_info

    async def do_task(self):
        async with async_playwright() as self.playwright:
            self.chromium = self.playwright.chromium
            self.browser = await self.chromium.launch(proxy=self.proxy, headless=False)
            self.context = await self.browser.new_context(
                ignore_https_errors=True,
                viewport={"width": 1000, "height": 680},
                user_agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
            )
            # 先登录，通过上下文缓存登录状态
            self.page = await self.context.new_page()
            status = await self.loginAmazon(self.username, self.password, self.page)
            if status is None:
                return "登录未成功，请手动处理"
            logging.info("开始任务前，先清除购物车")
            await self.delete_all_goods()
            while True:
                if self.q.empty():
                    logger.info("任务全部完成")
                    break
                else:
                    tasks = []
                    if self.q.qsize() < 5:
                        for i in range(0, self.q.qsize()):
                            tasks.append(self.start_test_code(await self.context.new_page(), self.q.get()))
                    else:
                        for j in range(0, 5):
                            tasks.append(self.start_test_code(await self.context.new_page(), self.q.get()))
                    result = await asyncio.gather(*tasks)
                    self.results.extend(result)
                    await self.delete_tasks_goods()
            self.status_with_url = []
            await self.delete_all_goods()
            await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            return [result for result in self.results]

