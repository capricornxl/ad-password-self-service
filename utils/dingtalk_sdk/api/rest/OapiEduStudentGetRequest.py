"""
Created by auto_sdk on 2020.06.09
"""
from api.base import RestApi


class OapiEduStudentGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.class_id = None
        self.student_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.student.get'
