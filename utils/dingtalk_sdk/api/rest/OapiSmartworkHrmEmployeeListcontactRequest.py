"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiSmartworkHrmEmployeeListcontactRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.employee.listcontact'
