"""
Created by auto_sdk on 2019.11.14
"""
from api.base import RestApi


class OapiEduFaceGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.class_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.face.get'
