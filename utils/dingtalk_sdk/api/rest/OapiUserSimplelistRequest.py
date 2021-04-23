"""
Created by auto_sdk on 2018.08.13
"""
from api.base import RestApi


class OapiUserSimplelistRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.department_id = None
        self.lang = None
        self.offset = None
        self.order = None
        self.size = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.user.simplelist'
