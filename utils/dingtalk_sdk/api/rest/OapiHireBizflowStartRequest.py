"""
Created by auto_sdk on 2020.09.21
"""
from api.base import RestApi


class OapiHireBizflowStartRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.job_id = None
        self.op_userid = None
        self.resume_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.hire.bizflow.start'
