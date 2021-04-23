"""
Created by auto_sdk on 2019.12.20
"""
from api.base import RestApi


class OapiProcessinstanceCspaceInfoRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.processinstance.cspace.info'
