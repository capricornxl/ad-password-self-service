"""
Created by auto_sdk on 2019.09.16
"""
from api.base import RestApi


class OapiInactiveUserGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.offset = None
        self.query_date = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.inactive.user.get'
