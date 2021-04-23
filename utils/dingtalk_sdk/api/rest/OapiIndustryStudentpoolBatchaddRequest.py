"""
Created by auto_sdk on 2020.01.14
"""
from api.base import RestApi


class OapiIndustryStudentpoolBatchaddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.student_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.industry.studentpool.batchadd'
