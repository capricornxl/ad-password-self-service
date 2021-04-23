"""
Created by auto_sdk on 2020.02.27
"""
from api.base import RestApi


class OapiAttendanceGetupdatedataRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None
        self.work_date = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.getupdatedata'
