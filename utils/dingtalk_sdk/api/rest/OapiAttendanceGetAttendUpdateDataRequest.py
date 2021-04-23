"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiAttendanceGetAttendUpdateDataRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None
        self.work_date = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.getAttendUpdateData'
