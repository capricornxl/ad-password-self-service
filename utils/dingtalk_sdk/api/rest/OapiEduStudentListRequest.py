"""
Created by auto_sdk on 2020.06.09
"""
from api.base import RestApi


class OapiEduStudentListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.class_id = None
        self.page_no = None
        self.page_size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.student.list'
