"""
Created by auto_sdk on 2020.03.03
"""
from api.base import RestApi


class OapiRobotMessageSendgroupRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.msg_key = None
        self.msg_param = None
        self.token = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.robot.message.sendgroup'
