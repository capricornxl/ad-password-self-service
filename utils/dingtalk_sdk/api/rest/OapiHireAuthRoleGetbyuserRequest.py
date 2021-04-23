"""
Created by auto_sdk on 2021.02.03
"""
from api.base import RestApi


class OapiHireAuthRoleGetbyuserRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.hire.auth.role.getbyuser'
