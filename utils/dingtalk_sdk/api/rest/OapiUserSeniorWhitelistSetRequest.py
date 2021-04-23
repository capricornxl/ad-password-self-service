"""
Created by auto_sdk on 2020.09.15
"""
from api.base import RestApi


class OapiUserSeniorWhitelistSetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.senior_whitelist_request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.user.senior.whitelist.set'
