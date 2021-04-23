"""
Created by auto_sdk on 2021.02.25
"""
from api.base import RestApi


class OapiAttendanceGroupsIdtokeyRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.group_id = None
        self.op_user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.groups.idtokey'
