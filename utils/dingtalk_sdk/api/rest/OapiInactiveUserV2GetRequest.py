"""
Created by auto_sdk on 2020.01.13
"""
from api.base import RestApi


class OapiInactiveUserV2GetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dept_ids = None
        self.is_active = None
        self.offset = None
        self.query_date = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.inactive.user.v2.get'
