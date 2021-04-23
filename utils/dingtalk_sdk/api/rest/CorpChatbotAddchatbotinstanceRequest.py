"""
Created by auto_sdk on 2020.09.18
"""
from api.base import RestApi


class CorpChatbotAddchatbotinstanceRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatbot_id = None
        self.icon_media_id = None
        self.name = None
        self.open_conversation_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.chatbot.addchatbotinstance'
