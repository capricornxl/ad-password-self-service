"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiDepartmentListParentDeptsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userId = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.department.list_parent_depts'
