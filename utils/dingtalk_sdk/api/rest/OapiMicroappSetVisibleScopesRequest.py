"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiMicroappSetVisibleScopesRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentId = None
        self.deptVisibleScopes = None
        self.isHidden = None
        self.userVisibleScopes = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.microapp.set_visible_scopes'
