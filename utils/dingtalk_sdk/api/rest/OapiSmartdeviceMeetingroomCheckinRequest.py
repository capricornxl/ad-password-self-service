"""
Created by auto_sdk on 2020.11.05
"""
from api.base import RestApi


class OapiSmartdeviceMeetingroomCheckinRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.bookid = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.meetingroom.checkin'
