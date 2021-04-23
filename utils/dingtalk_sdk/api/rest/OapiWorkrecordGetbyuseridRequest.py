"""
Created by auto_sdk on 2021.04.12
"""
from api.base import RestApi


class OapiWorkrecordGetbyuseridRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.limit = None
        self.offset = None
        self.status = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workrecord.getbyuserid'
