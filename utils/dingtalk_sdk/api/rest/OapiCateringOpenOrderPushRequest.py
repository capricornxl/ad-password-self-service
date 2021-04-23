"""
Created by auto_sdk on 2021.03.10
"""
from api.base import RestApi


class OapiCateringOpenOrderPushRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.actual_amount = None
        self.allowance_amount = None
        self.ext = None
        self.meal_plan_no = None
        self.meal_time = None
        self.order_details = None
        self.order_full_amount = None
        self.order_id = None
        self.order_time = None
        self.shop_id = None
        self.shop_name = None
        self.user_name = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.catering.open.order.push'
