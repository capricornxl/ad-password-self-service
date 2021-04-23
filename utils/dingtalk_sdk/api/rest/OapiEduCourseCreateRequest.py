"""
Created by auto_sdk on 2021.04.14
"""
from api.base import RestApi


class OapiEduCourseCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_key = None
        self.end_time = None
        self.introduce = None
        self.name = None
        self.op_userid = None
        self.option = None
        self.start_time = None
        self.teacher_corpid = None
        self.teacher_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.course.create'
