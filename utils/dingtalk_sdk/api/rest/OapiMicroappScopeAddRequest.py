"""
Created by auto_sdk on 2020.08.06
"""
from api.base import RestApi


class OapiMicroappScopeAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.microapp.scope.add'
