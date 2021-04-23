"""
Created by auto_sdk on 2019.10.08
"""
from api.base import RestApi


class OapiCspaceAuthGenerateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.app_id = None
        self.duration = None
        self.file_ids = None
        self.path = None
        self.type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.cspace.auth.generate'
