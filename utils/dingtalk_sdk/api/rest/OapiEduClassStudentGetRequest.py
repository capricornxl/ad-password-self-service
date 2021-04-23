"""
Created by auto_sdk on 2020.06.11
"""
from api.base import RestApi


class OapiEduClassStudentGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.class_id = None
        self.student_param = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.class.student.get'
