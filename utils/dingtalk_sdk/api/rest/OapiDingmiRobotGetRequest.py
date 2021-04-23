"""
Created by auto_sdk on 2020.09.23
"""
from api.base import RestApi


class OapiDingmiRobotGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingmi.robot.get'
