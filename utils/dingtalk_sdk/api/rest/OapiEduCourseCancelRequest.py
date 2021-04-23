"""
Created by auto_sdk on 2021.04.14
"""
from api.base import RestApi


class OapiEduCourseCancelRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.course_code = None
        self.op_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.course.cancel'
