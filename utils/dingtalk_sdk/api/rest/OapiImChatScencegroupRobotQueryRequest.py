"""
Created by auto_sdk on 2021.02.26
"""
from api.base import RestApi


class OapiImChatScencegroupRobotQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open_conversation_id = None
        self.robot_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scencegroup.robot.query'
