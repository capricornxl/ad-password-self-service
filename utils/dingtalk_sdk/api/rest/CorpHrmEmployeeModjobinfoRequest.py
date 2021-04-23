"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpHrmEmployeeModjobinfoRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.hrm_api_job_model = None
        self.op_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.hrm.employee.modjobinfo'
