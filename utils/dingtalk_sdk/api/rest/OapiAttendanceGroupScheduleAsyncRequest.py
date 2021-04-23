"""
Created by auto_sdk on 2021.01.27
"""
from api.base import RestApi


class OapiAttendanceGroupScheduleAsyncRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.group_id = None
        self.op_user_id = None
        self.schedules = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.group.schedule.async'
