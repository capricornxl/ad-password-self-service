"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiUserGetUseridByUnionidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.unionid = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.user.getUseridByUnionid'
