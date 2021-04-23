"""
Created by auto_sdk on 2019.08.30
"""
from api.base import RestApi


class OapiBipaasGenericRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.bipaas.generic'
