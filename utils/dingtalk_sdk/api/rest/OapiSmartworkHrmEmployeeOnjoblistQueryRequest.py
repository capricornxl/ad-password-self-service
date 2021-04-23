"""
Created by auto_sdk on 2021.01.08
"""
from api.base import RestApi


class OapiSmartworkHrmEmployeeOnjoblistQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.search_param = None
        self.size = None
        self.status_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.employee.onjoblist.query'
