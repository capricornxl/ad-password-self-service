"""
Created by auto_sdk on 2020.10.12
"""
from api.base import RestApi


class OapiImChatScenegroupUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chat_banned_type = None
        self.icon = None
        self.management_type = None
        self.mention_all_authority = None
        self.open_conversation_id = None
        self.owner_user_id = None
        self.searchable = None
        self.show_history_type = None
        self.title = None
        self.validation_type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scenegroup.update'
