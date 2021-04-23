"""
Created by auto_sdk on 2020.05.29
"""
from api.base import RestApi


class OapiPbpEventSyncRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.pbp.event.sync'
