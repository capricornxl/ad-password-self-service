"""
Created by auto_sdk on 2020.12.22
"""
from api.base import RestApi


class OapiProjectPointRuleListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.tenant_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.project.point.rule.list'
