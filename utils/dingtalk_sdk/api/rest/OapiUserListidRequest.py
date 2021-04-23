"""
Created by auto_sdk on 2020.09.13
"""
from api.base import RestApi


class OapiUserListidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dept_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.user.listid'
