"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiUserGetDeptMemberRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.deptId = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.user.getDeptMember'
