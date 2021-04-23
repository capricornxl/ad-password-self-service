"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class CorpChatbotCreateorgbotRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.create_chat_bot_model = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.chatbot.createorgbot'
