"""
Created by auto_sdk on 2019.11.25
"""
from api.base import RestApi


class OapiAttendanceGetcolumnvalRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.column_id_list = None
        self.from_date = None
        self.to_date = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.getcolumnval'
