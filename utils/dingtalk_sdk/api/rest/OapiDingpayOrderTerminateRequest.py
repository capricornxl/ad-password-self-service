"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiDingpayOrderTerminateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.extension = None
        self.operator = None
        self.order_nos = None
        self.reason = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingpay.order.terminate'
