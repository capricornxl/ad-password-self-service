"""
Created by auto_sdk on 2020.08.03
"""
from api.base import RestApi


class OapiWorkspaceCircleGroupListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.circle.group.list'
