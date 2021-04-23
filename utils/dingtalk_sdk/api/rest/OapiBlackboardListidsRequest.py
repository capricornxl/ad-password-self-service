"""
Created by auto_sdk on 2020.07.29
"""
from api.base import RestApi


class OapiBlackboardListidsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.query_request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.blackboard.listids'
