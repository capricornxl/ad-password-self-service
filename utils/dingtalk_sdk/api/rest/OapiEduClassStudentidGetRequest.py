"""
Created by auto_sdk on 2020.08.29
"""
from api.base import RestApi


class OapiEduClassStudentidGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.app_id = None
        self.class_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.class.studentid.get'
