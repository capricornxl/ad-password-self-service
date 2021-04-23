"""
Created by auto_sdk on 2020.12.24
"""
from api.base import RestApi


class OapiEduStudentAttendanceStatisticsGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.date = None
        self.op_userid = None
        self.school_corpid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.student.attendance.statistics.get'
