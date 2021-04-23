"""
Created by auto_sdk on 2019.12.05
"""
from api.base import RestApi


class OapiAttendanceShiftUpdatepunchesRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.op_user_id = None
        self.punches = None
        self.shift_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.shift.updatepunches'
