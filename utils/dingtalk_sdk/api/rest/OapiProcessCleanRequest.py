"""
Created by auto_sdk on 2019.12.26
"""
from api.base import RestApi


class OapiProcessCleanRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.corpid = None
        self.process_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.clean'
