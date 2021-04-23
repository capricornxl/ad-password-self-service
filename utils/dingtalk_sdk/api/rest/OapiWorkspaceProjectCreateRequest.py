"""
Created by auto_sdk on 2020.01.09
"""
from api.base import RestApi


class OapiWorkspaceProjectCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.belong_corp_userid = None
        self.create_group = None
        self.desc = None
        self.name = None
        self.open_conversation_id = None
        self.outer_id = None
        self.template_id = None
        self.type = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.project.create'
