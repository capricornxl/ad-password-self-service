"""
Created by auto_sdk on 2020.10.26
"""
from api.base import RestApi


class OapiEduCourseDetaildataListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.category_code = None
        self.course_code = None
        self.cursor = None
        self.factor_codes = None
        self.op_userid = None
        self.size = None
        self.user_cropid = None
        self.user_ids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.course.detaildata.list'
