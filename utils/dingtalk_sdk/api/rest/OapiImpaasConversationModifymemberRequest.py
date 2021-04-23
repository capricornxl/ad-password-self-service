"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiImpaasConversationModifymemberRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.channel = None
        self.chatid = None
        self.memberid_list = None
        self.type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.impaas.conversation.modifymember'
