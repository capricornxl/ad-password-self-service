"""
Created by auto_sdk on 2020.12.29
"""
from api.base import RestApi


class OapiEduCardUserTaskSubmitRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.taskparam = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.card.user.task.submit'
