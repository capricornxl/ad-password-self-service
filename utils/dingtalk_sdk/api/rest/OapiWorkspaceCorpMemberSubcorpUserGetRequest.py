"""
Created by auto_sdk on 2020.09.15
"""
from api.base import RestApi


class OapiWorkspaceCorpMemberSubcorpUserGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.belong_org_userids = None
        self.target_corp_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.corp.member.subcorp.user.get'
