"""
Created by auto_sdk on 2021.04.15
"""
from api.base import RestApi


class OapiEduTeacherCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.adviser = None
        self.biz_id = None
        self.class_id = None
        self.operator = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.teacher.create'
