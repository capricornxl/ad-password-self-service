"""
Created by auto_sdk on 2020.11.09
"""
from api.base import RestApi


class OapiRobotOrgIntelligentMessageSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.at_user_ids = None
        self.msg_key = None
        self.msg_param = None
        self.open_conversation_id = None
        self.receiver_user_ids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.robot.org.intelligent.message.send'
