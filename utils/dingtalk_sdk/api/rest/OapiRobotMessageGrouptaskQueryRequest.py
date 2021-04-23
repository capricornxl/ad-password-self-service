"""
Created by auto_sdk on 2020.03.03
"""
from api.base import RestApi


class OapiRobotMessageGrouptaskQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.process_query_key = None
        self.token = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.robot.message.grouptask.query'
