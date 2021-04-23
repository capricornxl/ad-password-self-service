"""
Created by auto_sdk on 2020.11.17
"""
from api.base import RestApi


class OapiMicroappCheckuidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.microapp.checkuid'
