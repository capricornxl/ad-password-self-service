"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiCorpConversationMemberListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chat_id = None
        self.offset = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.corp.conversation.member.list'
