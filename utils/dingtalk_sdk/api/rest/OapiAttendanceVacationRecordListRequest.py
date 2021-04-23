"""
Created by auto_sdk on 2020.04.09
"""
from api.base import RestApi


class OapiAttendanceVacationRecordListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.leave_code = None
        self.offset = None
        self.op_userid = None
        self.size = None
        self.userids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.vacation.record.list'
