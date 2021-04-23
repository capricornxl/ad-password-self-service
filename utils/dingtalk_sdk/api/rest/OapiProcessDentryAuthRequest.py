"""
Created by auto_sdk on 2020.11.23
"""
from api.base import RestApi


class OapiProcessDentryAuthRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.dentry.auth'
