"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiMessageSendToSingleConversationRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.msg = None
        self.receiver_userid = None
        self.sender_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.message.send_to_single_conversation'
