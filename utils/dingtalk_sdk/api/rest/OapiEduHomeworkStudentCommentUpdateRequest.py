"""
Created by auto_sdk on 2020.04.29
"""
from api.base import RestApi


class OapiEduHomeworkStudentCommentUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.attributes = None
        self.biz_code = None
        self.class_id = None
        self.comment = None
        self.comment_id = None
        self.hw_id = None
        self.media = None
        self.photo = None
        self.student_id = None
        self.student_name = None
        self.teacher_userid = None
        self.video = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.homework.student.comment.update'
