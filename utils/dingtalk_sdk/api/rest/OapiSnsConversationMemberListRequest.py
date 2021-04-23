"""
Created by auto_sdk on 2020.10.15
"""
from api.base import RestApi


class OapiSnsConversationMemberListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.open_conversation_id = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.sns.conversation.member.list'
