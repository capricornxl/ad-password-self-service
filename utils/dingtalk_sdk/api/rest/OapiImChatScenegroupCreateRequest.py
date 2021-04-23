"""
Created by auto_sdk on 2021.03.01
"""
from api.base import RestApi


class OapiImChatScenegroupCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chat_banned_type = None
        self.icon = None
        self.management_type = None
        self.mention_all_authority = None
        self.owner_user_id = None
        self.searchable = None
        self.show_history_type = None
        self.subadmin_ids = None
        self.template_id = None
        self.title = None
        self.user_ids = None
        self.uuid = None
        self.validation_type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scenegroup.create'
