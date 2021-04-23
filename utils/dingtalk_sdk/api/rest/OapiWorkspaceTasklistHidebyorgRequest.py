"""
Created by auto_sdk on 2021.01.04
"""
from api.base import RestApi


class OapiWorkspaceTasklistHidebyorgRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.microapp_agent_id = None
        self.operator_userid = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.tasklist.hidebyorg'
