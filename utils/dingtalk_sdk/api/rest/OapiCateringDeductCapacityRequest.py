"""
Created by auto_sdk on 2021.03.10
"""
from api.base import RestApi


class OapiCateringDeductCapacityRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.mea_time = None
        self.order_full_amount = None
        self.orderid = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.catering.deduct.capacity'
