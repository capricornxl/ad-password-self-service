"""
Created by auto_sdk on 2019.11.01
"""
from api.base import RestApi


class OapiBipaasDiAgentRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.bipaas.di.agent'
