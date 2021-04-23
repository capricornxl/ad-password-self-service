"""
Created by auto_sdk on 2019.09.24
"""
from api.base import RestApi


class OapiChatBanwordsQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatid = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.banwords.query'
