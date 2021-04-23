"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiDingpayOrderMarkotherpayRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.apply_pay_operator_userid = None
        self.extension = None
        self.order_nos = None
        self.pay_channel_payer_real_uid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingpay.order.markotherpay'
