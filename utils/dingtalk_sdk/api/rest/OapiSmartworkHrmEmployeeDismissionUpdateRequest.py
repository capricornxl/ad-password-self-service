"""
Created by auto_sdk on 2020.07.16
"""
from api.base import RestApi


class OapiSmartworkHrmEmployeeDismissionUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.employee.dismission.update'
