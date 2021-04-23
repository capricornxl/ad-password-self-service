"""
Created by auto_sdk on 2019.08.16
"""
from api.base import RestApi


class OapiAttendanceGroupMemberUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.group_id = None
        self.op_user_id = None
        self.schedule_flag = None
        self.update_param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.group.member.update'
