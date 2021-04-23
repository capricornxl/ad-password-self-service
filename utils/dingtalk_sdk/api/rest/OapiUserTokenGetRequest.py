"""
Created by auto_sdk on 2021.01.20
"""
from api.base import RestApi


class OapiUserTokenGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.user.token.get'
