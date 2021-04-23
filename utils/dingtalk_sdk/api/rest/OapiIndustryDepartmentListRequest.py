"""
Created by auto_sdk on 2020.08.05
"""
from api.base import RestApi


class OapiIndustryDepartmentListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.dept_id = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.industry.department.list'
