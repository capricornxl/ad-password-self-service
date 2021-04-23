"""
Created by auto_sdk on 2021.04.13
"""
from api.base import RestApi


class OapiAttendanceVacationTypeCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_type = None
        self.extras = None
        self.freedom_leave = None
        self.hours_in_per_day = None
        self.leave_name = None
        self.leave_time_ceil = None
        self.leave_time_ceil_min_unit = None
        self.leave_view_unit = None
        self.min_leave_hour = None
        self.natural_day_leave = None
        self.op_userid = None
        self.paid_leave = None
        self.visibility_rules = None
        self.when_can_leave = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.vacation.type.create'
