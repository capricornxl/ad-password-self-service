"""
Created by auto_sdk on 2019.10.15
"""
from api.base import RestApi


class OapiSmartdevicePrintdetailGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.printdetail.get'
