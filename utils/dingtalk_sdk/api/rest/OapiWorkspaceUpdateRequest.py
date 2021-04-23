"""
Created by auto_sdk on 2020.01.17
"""
from api.base import RestApi


class OapiWorkspaceUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.update_info = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.update'
