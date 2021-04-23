"""
Created by auto_sdk on 2020.12.24
"""
from api.base import RestApi


class OapiProjectPointAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.action_time = None
        self.rule_code = None
        self.rule_name = None
        self.score = None
        self.tenant_id = None
        self.userid = None
        self.uuid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.project.point.add'
