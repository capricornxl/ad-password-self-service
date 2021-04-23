"""
Created by auto_sdk on 2020.08.05
"""
from api.base import RestApi


class OapiIndustryOrganizationGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.industry.organization.get'
