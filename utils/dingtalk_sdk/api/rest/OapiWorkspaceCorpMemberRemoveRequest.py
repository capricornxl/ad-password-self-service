"""
Created by auto_sdk on 2020.03.15
"""
from api.base import RestApi


class OapiWorkspaceCorpMemberRemoveRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.target_corp_id = None
        self.userids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.corp.member.remove'
