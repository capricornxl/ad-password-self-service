"""
Created by auto_sdk on 2020.10.20
"""
from api.base import RestApi


class OapiEduCourseStartRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.course_code = None
        self.op_user_id = None
        self.start_option = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.course.start'
