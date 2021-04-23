"""
Created by auto_sdk on 2020.03.02
"""
from api.base import RestApi


class OapiSmartworkHrmEmployeeListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.field_filter_list = None
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.employee.list'
