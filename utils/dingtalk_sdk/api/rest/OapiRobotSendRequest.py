"""
Created by auto_sdk on 2021.03.30
"""
from api.base import RestApi


class OapiRobotSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.actionCard = None
        self.at = None
        self.feedCard = None
        self.link = None
        self.markdown = None
        self.msgtype = None
        self.text = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.robot.send'
