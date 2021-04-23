"""
Created by auto_sdk on 2019.10.09
"""
from api.base import RestApi


class OapiAttendanceGetattcolumnsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.getattcolumns'
