"""
Created by auto_sdk on 2020.03.25
"""
from api.base import RestApi


class OapiWorkspaceCorpMemberGetuseridsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.source_corp_id = None
        self.userids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.corp.member.getuserids'
