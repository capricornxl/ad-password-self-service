"""
Created by auto_sdk on 2021.02.24
"""
from api.base import RestApi


class OapiSmartworkHrmOrganizationDeptUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.attributeVOS = None
        self.dept_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.organization.dept.update'
