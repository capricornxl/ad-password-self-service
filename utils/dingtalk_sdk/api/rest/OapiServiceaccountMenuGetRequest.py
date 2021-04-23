"""
Created by auto_sdk on 2019.07.05
"""
from api.base import RestApi


class OapiServiceaccountMenuGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.serviceaccount.menu.get'
