"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiServiceActivateSuiteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.auth_corpid = None
        self.permanent_code = None
        self.suite_key = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.service.activate_suite'
