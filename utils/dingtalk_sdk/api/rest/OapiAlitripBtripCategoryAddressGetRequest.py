"""
Created by auto_sdk on 2018.08.07
"""
from api.base import RestApi


class OapiAlitripBtripCategoryAddressGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.rq = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.alitrip.btrip.category.address.get'
