"""
Created by auto_sdk on 2019.11.19
"""
from api.base import RestApi


class OapiAttendanceFaceRecognitionRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.media_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.attendance.face.recognition'
