"""
Created by auto_sdk on 2020.07.07
"""
from api.base import RestApi


class OapiServiceGetSuiteTokenRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.suite_key = None
        self.suite_secret = None
        self.suite_ticket = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.service.get_suite_token'
