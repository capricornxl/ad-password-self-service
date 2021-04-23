"""
Created by auto_sdk on 2021.04.15
"""
from api.base import RestApi


class OapiEduGradeCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open_grade = None
        self.operator = None
        self.super_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.grade.create'
