"""
Created by auto_sdk on 2020.11.03
"""
from api.base import RestApi


class OapiAttendanceAdvancedServiceUnbindRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.entity_id = None
        self.entity_type = None
        self.op_userid = None
        self.service_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.advanced.service.unbind'
