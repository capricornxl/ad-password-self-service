"""
Created by auto_sdk on 2021.01.14
"""
from api.base import RestApi


class OapiV2UserDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.v2.user.delete'
