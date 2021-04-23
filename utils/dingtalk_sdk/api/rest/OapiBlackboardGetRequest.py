"""
Created by auto_sdk on 2020.07.29
"""
from api.base import RestApi


class OapiBlackboardGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.blackboard_id = None
        self.operation_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.blackboard.get'
