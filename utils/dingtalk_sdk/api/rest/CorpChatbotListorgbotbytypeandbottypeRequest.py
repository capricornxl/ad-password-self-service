"""
Created by auto_sdk on 2020.09.18
"""
from api.base import RestApi


class CorpChatbotListorgbotbytypeandbottypeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.bot_type = None
        self.type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.chatbot.listorgbotbytypeandbottype'
