"""
Created by auto_sdk on 2020.09.13
"""
from api.base import RestApi


class OapiV2UserGetbymobileRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.v2.user.getbymobile'
