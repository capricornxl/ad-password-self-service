"""
Created by auto_sdk on 2020.10.13
"""
from api.base import RestApi


class OapiV2DepartmentListsubRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dept_id = None
        self.language = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.v2.department.listsub'
