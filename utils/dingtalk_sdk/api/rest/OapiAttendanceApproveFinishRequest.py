"""
Created by auto_sdk on 2021.03.03
"""
from api.base import RestApi


class OapiAttendanceApproveFinishRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.approve_id = None
        self.biz_type = None
        self.calculate_model = None
        self.dingtalk_approve_id = None
        self.duration_unit = None
        self.from_time = None
        self.jump_url = None
        self.overtime_duration = None
        self.overtime_to_more = None
        self.sub_type = None
        self.tag_name = None
        self.to_time = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.approve.finish'
