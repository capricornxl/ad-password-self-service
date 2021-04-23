"""
Created by auto_sdk on 2020.09.16
"""
from api.base import RestApi


class OapiIndustryUserListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.dept_id = None
        self.role = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.industry.user.list'
