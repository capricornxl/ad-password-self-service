"""
Created by auto_sdk on 2020.04.28
"""
from api.base import RestApi


class OapiEduHomeworkStudentSubmitRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.attributes = None
        self.biz_code = None
        self.class_id = None
        self.content = None
        self.hw_id = None
        self.media = None
        self.photo = None
        self.student_id = None
        self.student_name = None
        self.submitor_id = None
        self.title = None
        self.video = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.homework.student.submit'
