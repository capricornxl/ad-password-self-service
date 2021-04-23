"""
Created by auto_sdk on 2019.09.24
"""
from api.base import RestApi


class OapiAttendanceGetleavetimebynamesRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.from_date = None
        self.leave_names = None
        self.to_date = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.getleavetimebynames'
