"""
Created by auto_sdk on 2019.12.16
"""
from api.base import RestApi


class OapiHrmEmployeeModjobinfoRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.hrm_api_job_model = None
        self.op_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.hrm.employee.modjobinfo'
