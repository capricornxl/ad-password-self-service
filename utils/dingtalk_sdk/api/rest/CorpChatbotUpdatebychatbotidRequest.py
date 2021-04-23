"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpChatbotUpdatebychatbotidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.breif = None
        self.chatbot_id = None
        self.description = None
        self.icon = None
        self.name = None
        self.preview_media_id = None
        self.update_type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.chatbot.updatebychatbotid'
