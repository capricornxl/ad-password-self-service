"""
Created by auto_sdk on 2019.09.25
"""
from api.base import RestApi


class OapiAttendanceApproveDurationCalculateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_type = None
        self.calculate_model = None
        self.duration_unit = None
        self.from_time = None
        self.to_time = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.approve.duration.calculate'
