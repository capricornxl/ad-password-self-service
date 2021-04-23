"""
Created by auto_sdk on 2020.04.16
"""
from api.base import RestApi


class OapiAlitripBtripMonthbillUrlGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.alitrip.btrip.monthbill.url.get'
