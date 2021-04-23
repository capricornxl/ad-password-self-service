"""
Created by auto_sdk on 2020.04.28
"""
from api.base import RestApi


class OapiEduHomeworkGroupRoleGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.homework.group.role.get'
