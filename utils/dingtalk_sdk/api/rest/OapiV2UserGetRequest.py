"""
Created by auto_sdk on 2021.03.29
"""
from api.base import RestApi


class OapiV2UserGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.language = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.v2.user.get'
