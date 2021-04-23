"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiSmartworkHrmEmployeeQueryonjobRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.offset = None
        self.size = None
        self.status_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.employee.queryonjob'
