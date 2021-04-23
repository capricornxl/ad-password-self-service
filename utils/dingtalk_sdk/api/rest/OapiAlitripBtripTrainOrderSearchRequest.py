"""
Created by auto_sdk on 2021.01.28
"""
from api.base import RestApi


class OapiAlitripBtripTrainOrderSearchRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.rq = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.alitrip.btrip.train.order.search'
