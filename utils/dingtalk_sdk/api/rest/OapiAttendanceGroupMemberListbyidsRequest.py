"""
Created by auto_sdk on 2019.08.16
"""
from api.base import RestApi


class OapiAttendanceGroupMemberListbyidsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.group_id = None
        self.member_ids = None
        self.member_type = None
        self.op_user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.group.member.listbyids'
