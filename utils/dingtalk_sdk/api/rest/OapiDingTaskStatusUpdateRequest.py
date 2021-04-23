"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiDingTaskStatusUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.operator_userid = None
        self.task_id = None
        self.task_status = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ding.task.status.update'
