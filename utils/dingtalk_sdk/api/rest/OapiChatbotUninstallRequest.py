"""
Created by auto_sdk on 2020.11.25
"""
from api.base import RestApi


class OapiChatbotUninstallRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatbot_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chatbot.uninstall'
