"""
Created by auto_sdk on 2020.02.17
"""
from api.base import RestApi


class OapiWorkspaceStatusUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.update_status = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.status.update'
