"""
Created by auto_sdk on 2019.12.30
"""
from api.base import RestApi


class OapiProcessDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.delete'
