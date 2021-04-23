"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiMicroappAddwithuseridRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentId = None
        self.userids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.microapp.addwithuserid'
