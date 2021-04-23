"""
Created by auto_sdk on 2020.08.10
"""
from api.base import RestApi


class OapiEduCourseUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.course_code = None
        self.end_time = None
        self.introduce = None
        self.name = None
        self.op_userid = None
        self.start_time = None
        self.teacher_corpid = None
        self.teacher_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.course.update'
