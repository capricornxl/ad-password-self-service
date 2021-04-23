"""
Created by auto_sdk on 2020.11.12
"""
from api.base import RestApi


class OapiMicroappCustomDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.app_corp_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.microapp.custom.delete'
