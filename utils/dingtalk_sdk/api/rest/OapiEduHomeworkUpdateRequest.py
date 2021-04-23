"""
Created by auto_sdk on 2020.04.29
"""
from api.base import RestApi


class OapiEduHomeworkUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.hw_id = None
        self.identifier = None
        self.status = None
        self.teacher_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.homework.update'
