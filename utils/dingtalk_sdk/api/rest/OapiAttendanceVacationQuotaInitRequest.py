"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiAttendanceVacationQuotaInitRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.leave_quotas = None
        self.op_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.vacation.quota.init'
