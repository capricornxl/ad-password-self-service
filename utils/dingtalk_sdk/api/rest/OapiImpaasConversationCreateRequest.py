"""
Created by auto_sdk on 2020.11.02
"""
from api.base import RestApi


class OapiImpaasConversationCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.channel = None
        self.name = None
        self.owner_userid = None
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.impaas.conversation.create'
