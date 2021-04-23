"""
Created by auto_sdk on 2020.06.01
"""
from api.base import RestApi


class OapiPbpEventDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.pbp.event.delete'
