"""
Created by auto_sdk on 2019.07.31
"""
from api.base import RestApi


class OapiAttendanceGroupMemberusersListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.group_id = None
        self.op_user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.group.memberusers.list'
