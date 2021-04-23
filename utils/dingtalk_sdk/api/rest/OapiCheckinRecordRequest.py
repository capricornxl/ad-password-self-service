"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiCheckinRecordRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.department_id = None
        self.end_time = None
        self.offset = None
        self.order = None
        self.size = None
        self.start_time = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.checkin.record'
