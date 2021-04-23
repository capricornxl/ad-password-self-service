"""
Created by auto_sdk on 2021.03.10
"""
from api.base import RestApi


class OapiV2UserListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.contain_access_limit = None
        self.cursor = None
        self.dept_id = None
        self.language = None
        self.order_field = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.v2.user.list'
