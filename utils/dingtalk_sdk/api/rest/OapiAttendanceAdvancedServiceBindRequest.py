"""
Created by auto_sdk on 2020.11.03
"""
from api.base import RestApi


class OapiAttendanceAdvancedServiceBindRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.op_userid = None
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.advanced.service.bind'
