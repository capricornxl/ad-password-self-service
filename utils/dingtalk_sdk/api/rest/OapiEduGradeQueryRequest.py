"""
Created by auto_sdk on 2020.10.28
"""
from api.base import RestApi


class OapiEduGradeQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.campus_id = None
        self.operator = None
        self.period_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.grade.query'
