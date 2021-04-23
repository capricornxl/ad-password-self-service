"""
Created by auto_sdk on 2020.11.06
"""
from api.base import RestApi


class OapiWorkspaceCircleTagCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.req = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.circle.tag.create'
