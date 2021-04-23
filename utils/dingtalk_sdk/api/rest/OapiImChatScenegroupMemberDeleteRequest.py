"""
Created by auto_sdk on 2020.09.26
"""
from api.base import RestApi


class OapiImChatScenegroupMemberDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.contact_staff_ids = None
        self.open_conversation_id = None
        self.user_ids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scenegroup.member.delete'
