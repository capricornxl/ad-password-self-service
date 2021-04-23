"""
Created by auto_sdk on 2020.07.09
"""
from api.base import RestApi


class OapiCheckinRecordGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.end_time = None
        self.size = None
        self.start_time = None
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.checkin.record.get'
