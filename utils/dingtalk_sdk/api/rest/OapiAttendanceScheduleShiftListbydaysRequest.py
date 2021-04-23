"""
Created by auto_sdk on 2019.08.06
"""
from api.base import RestApi


class OapiAttendanceScheduleShiftListbydaysRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.from_date_time = None
        self.op_user_id = None
        self.to_date_time = None
        self.userids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.schedule.shift.listbydays'
