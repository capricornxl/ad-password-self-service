"""
Created by auto_sdk on 2021.03.17
"""
from api.base import RestApi


class OapiImChatbotDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatbot_user_id = None
        self.open_conversation_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chatbot.delete'
