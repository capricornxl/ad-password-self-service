"""
Created by auto_sdk on 2021.04.20
"""
from api.base import RestApi


class OapiEduCourseListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.end_time = None
        self.op_userid = None
        self.option = None
        self.participant_condition = None
        self.scene = None
        self.size = None
        self.start_time = None
        self.statuses = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.course.list'
