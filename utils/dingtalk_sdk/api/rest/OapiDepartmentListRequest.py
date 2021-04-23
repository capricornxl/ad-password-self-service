"""
Created by auto_sdk on 2019.12.17
"""
from api.base import RestApi


class OapiDepartmentListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.fetch_child = None
        self.id = None
        self.lang = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.department.list'
