"""
Created by auto_sdk on 2019.08.21
"""
from api.base import RestApi


class OapiAttendanceGroupMemberListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.group_id = None
        self.op_user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.group.member.list'
