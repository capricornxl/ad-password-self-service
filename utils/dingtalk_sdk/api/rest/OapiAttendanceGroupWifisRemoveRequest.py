"""
Created by auto_sdk on 2020.04.09
"""
from api.base import RestApi


class OapiAttendanceGroupWifisRemoveRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.group_key = None
        self.op_userid = None
        self.wifi_key_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.group.wifis.remove'
