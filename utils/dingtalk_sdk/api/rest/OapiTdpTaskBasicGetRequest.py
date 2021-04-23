"""
Created by auto_sdk on 2020.12.23
"""
from api.base import RestApi


class OapiTdpTaskBasicGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.microapp_agent_id = None
        self.task_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.tdp.task.basic.get'
