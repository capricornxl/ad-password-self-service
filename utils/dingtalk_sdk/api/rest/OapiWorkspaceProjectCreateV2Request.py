"""
Created by auto_sdk on 2021.02.23
"""
from api.base import RestApi


class OapiWorkspaceProjectCreateV2Request(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.belong_corp_userid = None
        self.create_group = None
        self.desc = None
        self.logo_media_id = None
        self.name = None
        self.open_conversation_id = None
        self.outer_id = None
        self.type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.project.create.v2'
