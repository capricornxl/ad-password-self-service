"""
Created by auto_sdk on 2021.01.26
"""
from api.base import RestApi


class OapiDingmiRobotUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.type = None
        self.update_bot_model = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingmi.robot.update'
