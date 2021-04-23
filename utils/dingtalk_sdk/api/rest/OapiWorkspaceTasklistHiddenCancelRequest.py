"""
Created by auto_sdk on 2020.12.23
"""
from api.base import RestApi


class OapiWorkspaceTasklistHiddenCancelRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.operator_userid = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.tasklist.hidden.cancel'
