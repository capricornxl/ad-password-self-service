"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiSsoGettokenRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.corpid = None
        self.corpsecret = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.sso.gettoken'
