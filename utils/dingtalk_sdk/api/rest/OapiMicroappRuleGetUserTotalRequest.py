"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiMicroappRuleGetUserTotalRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentId = None
        self.ruleIdList = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.microapp.rule.get_user_total'
