"""
Created by auto_sdk on 2020.06.05
"""
from api.base import RestApi


class OapiSmartworkHrmEmployeeUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.employee.update'
