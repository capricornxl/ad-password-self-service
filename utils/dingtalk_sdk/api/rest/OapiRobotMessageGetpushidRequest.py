"""
Created by auto_sdk on 2019.08.15
"""
from api.base import RestApi


class OapiRobotMessageGetpushidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.robot.message.getpushid'
