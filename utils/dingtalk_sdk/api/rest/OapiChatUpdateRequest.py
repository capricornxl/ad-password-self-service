"""
Created by auto_sdk on 2019.03.11
"""
from api.base import RestApi


class OapiChatUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.add_extidlist = None
        self.add_useridlist = None
        self.chatBannedType = None
        self.chatid = None
        self.del_extidlist = None
        self.del_useridlist = None
        self.icon = None
        self.isBan = None
        self.managementType = None
        self.mentionAllAuthority = None
        self.name = None
        self.owner = None
        self.ownerType = None
        self.searchable = None
        self.showHistoryType = None
        self.validationType = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.update'
