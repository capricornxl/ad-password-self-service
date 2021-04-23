"""
Created by auto_sdk on 2020.07.28
"""
from api.base import RestApi


class OapiAttendanceListRecordRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.checkDateFrom = None
        self.checkDateTo = None
        self.isI18n = None
        self.userIds = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.listRecord'
