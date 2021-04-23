"""
Created by auto_sdk on 2021.02.19
"""
from api.base import RestApi


class OapiSmartworkHrmOrganizationDeptGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dept_id = None
        self.field_code_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.organization.dept.get'
