"""
Created by auto_sdk on 2019.10.28
"""
from api.base import RestApi


class OapiAttendanceScheduleResultListbyidsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.op_user_id = None
        self.schedule_ids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.schedule.result.listbyids'
