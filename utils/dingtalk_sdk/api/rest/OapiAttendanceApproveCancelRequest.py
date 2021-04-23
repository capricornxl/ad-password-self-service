"""
Created by auto_sdk on 2021.03.03
"""
from api.base import RestApi


class OapiAttendanceApproveCancelRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.approve_id = None
        self.dingtalk_approve_id = None
        self.sub_type = None
        self.tag_name = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.approve.cancel'
