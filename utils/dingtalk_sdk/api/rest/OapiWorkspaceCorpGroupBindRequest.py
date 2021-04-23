"""
Created by auto_sdk on 2020.03.15
"""
from api.base import RestApi


class OapiWorkspaceCorpGroupBindRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chat_ids = None
        self.target_corp_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.corp.group.bind'
