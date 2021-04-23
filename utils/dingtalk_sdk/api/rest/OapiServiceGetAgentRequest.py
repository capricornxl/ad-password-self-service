"""
Created by auto_sdk on 2019.12.16
"""
from api.base import RestApi


class OapiServiceGetAgentRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.auth_corpid = None
        self.permanent_code = None
        self.suite_key = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.service.get_agent'
