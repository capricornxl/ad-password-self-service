"""
Created by auto_sdk on 2019.10.08
"""
from api.base import RestApi


class OapiCspaceAuthUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.duration = None
        self.isv_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.cspace.auth.update'
