"""
Created by auto_sdk on 2021.02.03
"""
from api.base import RestApi


class OapiDingmiCommonRobotAskRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.question = None
        self.robot_app_key = None
        self.session_uuid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingmi.common.robot.ask'
