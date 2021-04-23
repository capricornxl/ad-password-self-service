"""
Created by auto_sdk on 2019.09.03
"""
from api.base import RestApi


class OapiOpenencryptHeartbeatRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.appid = None
        self.extension = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.openencrypt.heartbeat'
