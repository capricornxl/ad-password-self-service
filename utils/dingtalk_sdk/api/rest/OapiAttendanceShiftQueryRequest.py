"""
Created by auto_sdk on 2020.11.20
"""
from api.base import RestApi


class OapiAttendanceShiftQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.op_user_id = None
        self.shift_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.shift.query'
