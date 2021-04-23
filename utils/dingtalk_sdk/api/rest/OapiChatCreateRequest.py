"""
Created by auto_sdk on 2019.03.11
"""
from api.base import RestApi


class OapiChatCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatBannedType = None
        self.conversationTag = None
        self.extidlist = None
        self.icon = None
        self.managementType = None
        self.mentionAllAuthority = None
        self.name = None
        self.owner = None
        self.ownerType = None
        self.searchable = None
        self.showHistoryType = None
        self.useridlist = None
        self.validationType = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.create'
