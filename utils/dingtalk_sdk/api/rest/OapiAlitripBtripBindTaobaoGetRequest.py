"""
Created by auto_sdk on 2020.02.19
"""
from api.base import RestApi


class OapiAlitripBtripBindTaobaoGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.alitrip.btrip.bind.taobao.get'
