"""
Created by auto_sdk on 2019.09.19
"""
from api.base import RestApi


class OapiAttendanceApproveScheduleSwitchRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.apply_shift_id = None
        self.apply_userid = None
        self.approve_id = None
        self.reback_apply_shift_id = None
        self.reback_date = None
        self.reback_target_shift_id = None
        self.switch_date = None
        self.target_shift_id = None
        self.target_userid = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.approve.schedule.switch'
