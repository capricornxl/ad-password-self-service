"""
Created by auto_sdk on 2020.02.06
"""
from api.base import RestApi


class OapiChatUpdatebanwordsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.ban_words_time = None
        self.chatid = None
        self.type = None
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.updatebanwords'
