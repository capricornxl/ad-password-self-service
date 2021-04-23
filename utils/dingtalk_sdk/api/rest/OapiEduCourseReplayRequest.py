"""
Created by auto_sdk on 2020.09.28
"""
from api.base import RestApi


class OapiEduCourseReplayRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.course_code = None
        self.op_user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.course.replay'
