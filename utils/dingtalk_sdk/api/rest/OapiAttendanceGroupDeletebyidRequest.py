"""
Created by auto_sdk on 2020.11.03
"""
from api.base import RestApi


class OapiAttendanceGroupDeletebyidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.group_id = None
        self.op_user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.group.deletebyid'
