"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiCspaceGrantCustomSpaceRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.domain = None
        self.duration = None
        self.fileids = None
        self.path = None
        self.type = None
        self.userid = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.cspace.grant_custom_space'
