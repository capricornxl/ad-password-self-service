"""
Created by auto_sdk on 2019.07.05
"""
from api.base import RestApi


class OapiServiceaccountMenuUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.menu = None
        self.unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.serviceaccount.menu.update'
