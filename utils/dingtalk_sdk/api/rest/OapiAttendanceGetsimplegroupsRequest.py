"""
Created by auto_sdk on 2020.12.17
"""
from api.base import RestApi


class OapiAttendanceGetsimplegroupsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.offset = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.getsimplegroups'
