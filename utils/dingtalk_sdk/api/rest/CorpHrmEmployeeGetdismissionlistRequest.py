"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpHrmEmployeeGetdismissionlistRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.current = None
        self.op_userid = None
        self.page_size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.hrm.employee.getdismissionlist'
