"""
Created by auto_sdk on 2021.04.01
"""
from api.base import RestApi


class OapiV2SafeSetdisableRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.reason = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.v2.safe.setdisable'
