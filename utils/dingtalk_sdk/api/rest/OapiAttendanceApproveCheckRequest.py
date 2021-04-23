"""
Created by auto_sdk on 2019.08.30
"""
from api.base import RestApi


class OapiAttendanceApproveCheckRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.approve_id = None
        self.jump_url = None
        self.punch_check_time = None
        self.punch_id = None
        self.tag_name = None
        self.user_check_time = None
        self.userid = None
        self.work_date = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.approve.check'
