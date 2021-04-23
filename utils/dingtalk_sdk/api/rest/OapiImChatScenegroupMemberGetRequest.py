"""
Created by auto_sdk on 2021.03.10
"""
from api.base import RestApi


class OapiImChatScenegroupMemberGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.open_conversation_id = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scenegroup.member.get'
