"""
Created by auto_sdk on 2021.02.19
"""
from api.base import RestApi


class OapiEduClassStudentBatchgetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request_param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.class.student.batchget'
