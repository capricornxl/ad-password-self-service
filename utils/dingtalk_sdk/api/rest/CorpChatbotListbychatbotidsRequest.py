"""
Created by auto_sdk on 2020.09.18
"""
from api.base import RestApi


class CorpChatbotListbychatbotidsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatbot_ids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.chatbot.listbychatbotids'
