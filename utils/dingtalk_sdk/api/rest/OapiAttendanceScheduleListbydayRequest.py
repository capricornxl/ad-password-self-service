"""
Created by auto_sdk on 2020.07.14
"""
from api.base import RestApi


class OapiAttendanceScheduleListbydayRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.date_time = None
        self.op_user_id = None
        self.user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.schedule.listbyday'
