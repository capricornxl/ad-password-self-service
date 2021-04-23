"""
Created by auto_sdk on 2019.08.01
"""
from api.base import RestApi


class OapiChatNickBatchupdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatid = None
        self.user_nick_model = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.nick.batchupdate'
