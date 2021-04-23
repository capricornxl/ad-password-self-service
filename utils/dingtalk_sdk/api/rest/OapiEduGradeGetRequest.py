"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiEduGradeGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.grade_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.grade.get'
