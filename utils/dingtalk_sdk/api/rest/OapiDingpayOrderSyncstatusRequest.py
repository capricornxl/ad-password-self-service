"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiDingpayOrderSyncstatusRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.order_nos = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingpay.order.syncstatus'
