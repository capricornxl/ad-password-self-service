"""
Created by auto_sdk on 2019.11.18
"""
from api.base import RestApi


class OapiDingTaskCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.task_send_v_o = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ding.task.create'
