"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiSmartworkHrmEmployeeQuerypreentryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.offset = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.employee.querypreentry'
