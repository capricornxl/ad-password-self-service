"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class CorpMessageCorpconversationSendmockRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.message = None
        self.message_type = None
        self.microapp_agent_id = None
        self.to_party = None
        self.to_user = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.message.corpconversation.sendmock'
