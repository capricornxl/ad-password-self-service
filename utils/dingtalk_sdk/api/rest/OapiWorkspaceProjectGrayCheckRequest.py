"""
Created by auto_sdk on 2021.02.04
"""
from api.base import RestApi


class OapiWorkspaceProjectGrayCheckRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.project.gray.check'
