"""
Created by auto_sdk on 2021.03.06
"""
from api.base import RestApi


class OapiRobotMessageOtotaskQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatbot_id = None
        self.process_query_key = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.robot.message.ototask.query'
