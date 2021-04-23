"""
Created by auto_sdk on 2021.02.22
"""
from api.base import RestApi


class OapiAttendanceGroupsQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.op_userid = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.groups.query'
