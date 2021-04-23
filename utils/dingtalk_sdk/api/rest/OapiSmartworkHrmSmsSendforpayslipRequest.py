"""
Created by auto_sdk on 2019.09.17
"""
from api.base import RestApi


class OapiSmartworkHrmSmsSendforpayslipRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.sms.sendforpayslip'
