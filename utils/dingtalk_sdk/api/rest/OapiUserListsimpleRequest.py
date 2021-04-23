"""
Created by auto_sdk on 2020.09.13
"""
from api.base import RestApi


class OapiUserListsimpleRequest(RestApi):
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
        return 'dingtalk.oapi.user.listsimple'
