"""
Created by auto_sdk on 2020.08.17
"""
from api.base import RestApi


class CorpChatbotInstallRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatbot_vo = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.chatbot.install'
