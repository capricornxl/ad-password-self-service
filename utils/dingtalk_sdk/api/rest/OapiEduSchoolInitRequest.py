"""
Created by auto_sdk on 2021.04.15
"""
from api.base import RestApi


class OapiEduSchoolInitRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.campus = None
        self.operator = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.school.init'
