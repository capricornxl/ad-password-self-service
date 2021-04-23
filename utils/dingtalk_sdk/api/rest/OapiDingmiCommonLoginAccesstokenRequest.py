"""
Created by auto_sdk on 2021.04.15
"""
from api.base import RestApi


class OapiDingmiCommonLoginAccesstokenRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.foreign_id = None
        self.nick = None
        self.source = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingmi.common.login.accesstoken'
