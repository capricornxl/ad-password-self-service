"""
Created by auto_sdk on 2020.12.28
"""
from api.base import RestApi


class OapiImChatScenegroupGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open_conversation_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scenegroup.get'
