"""
Created by auto_sdk on 2021.02.19
"""
from api.base import RestApi


class OapiImChatScencegroupMessageQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open_conversation_id = None
        self.open_msg_id = None
        self.sender_union_id = None
        self.sender_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scencegroup.message.query'
