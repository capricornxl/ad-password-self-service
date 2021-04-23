"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiAttendanceCorpInviteactiveAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.admin_mobile = None
        self.invited_mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.corp.inviteactive.add'
