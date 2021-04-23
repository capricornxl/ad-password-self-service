"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiCspaceAddToSingleChatRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.file_name = None
        self.media_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.cspace.add_to_single_chat'
