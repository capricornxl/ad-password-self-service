"""
Created by auto_sdk on 2020.01.09
"""
from api.base import RestApi


class OapiEduFaceSearchRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.class_id = None
        self.height = None
        self.synchronous = None
        self.url = None
        self.userid = None
        self.width = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.face.search'
