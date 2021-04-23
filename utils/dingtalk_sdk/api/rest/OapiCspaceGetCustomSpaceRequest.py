"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiCspaceGetCustomSpaceRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.domain = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.cspace.get_custom_space'
