"""
Created by auto_sdk on 2020.01.20
"""
from api.base import RestApi


class OapiAttendanceListscheduleRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.offset = None
        self.size = None
        self.workDate = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.listschedule'
