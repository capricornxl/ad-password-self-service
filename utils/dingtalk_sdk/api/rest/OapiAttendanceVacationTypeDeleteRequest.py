"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiAttendanceVacationTypeDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.leave_code = None
        self.op_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.vacation.type.delete'
