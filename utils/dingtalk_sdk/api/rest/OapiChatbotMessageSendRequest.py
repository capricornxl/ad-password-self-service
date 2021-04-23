"""
Created by auto_sdk on 2019.08.20
"""
from api.base import RestApi


class OapiChatbotMessageSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatbot_id = None
        self.message = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chatbot.message.send'
