"""
Created by auto_sdk on 2018.08.28
"""
from api.base import RestApi


class OapiGettokenRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.appkey = None
        self.appsecret = None
        self.corpid = None
        self.corpsecret = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.gettoken'
