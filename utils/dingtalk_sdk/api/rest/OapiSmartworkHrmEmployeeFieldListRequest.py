"""
Created by auto_sdk on 2019.12.26
"""
from api.base import RestApi


class OapiSmartworkHrmEmployeeFieldListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.employee.field.list'
