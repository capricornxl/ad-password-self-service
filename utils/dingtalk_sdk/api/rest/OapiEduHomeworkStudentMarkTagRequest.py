"""
Created by auto_sdk on 2020.11.03
"""
from api.base import RestApi


class OapiEduHomeworkStudentMarkTagRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.class_id = None
        self.hw_id = None
        self.student_id = None
        self.student_name = None
        self.tag = None
        self.teacher_id = None
        self.text = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.homework.student.mark.tag'
