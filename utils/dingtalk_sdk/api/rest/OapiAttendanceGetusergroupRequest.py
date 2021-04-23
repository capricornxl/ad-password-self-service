"""
Created by auto_sdk on 2020.01.19
"""
from api.base import RestApi


class OapiAttendanceGetusergroupRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.getusergroup'
