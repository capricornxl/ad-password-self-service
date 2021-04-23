"""
Created by auto_sdk on 2020.09.13
"""
from api.base import RestApi


class OapiUserGetbyunionidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.user.getbyunionid'
