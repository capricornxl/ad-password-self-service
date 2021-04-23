"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiSnsGettokenRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.appid = None
        self.appsecret = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.sns.gettoken'
