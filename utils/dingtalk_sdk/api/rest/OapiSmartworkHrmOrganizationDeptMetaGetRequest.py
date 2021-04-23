"""
Created by auto_sdk on 2021.01.26
"""
from api.base import RestApi


class OapiSmartworkHrmOrganizationDeptMetaGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.organization.dept.meta.get'
