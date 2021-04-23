"""
Created by auto_sdk on 2019.12.30
"""
from api.base import RestApi


class OapiSnsVerifyMobileRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.sns.verify_mobile'
