"""
Created by auto_sdk on 2021.02.24
"""
from api.base import RestApi


class OapiAlitripBtripAddressGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.alitrip.btrip.address.get'
