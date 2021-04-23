"""
Created by auto_sdk on 2020.01.14
"""
from api.base import RestApi


class OapiInspectFeedbackGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.form_id = None
        self.task_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.inspect.feedback.get'
