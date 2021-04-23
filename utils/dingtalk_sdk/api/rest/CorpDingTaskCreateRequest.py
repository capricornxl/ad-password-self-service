"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class CorpDingTaskCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.task_send_v_o = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.ding.task.create'
