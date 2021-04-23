"""
Created by auto_sdk on 2019.10.24
"""
from api.base import RestApi


class OapiAlitripBtripFlightCitySuggestRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.rq = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.alitrip.btrip.flight.city.suggest'
