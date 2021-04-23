"""
Created by auto_sdk on 2020.06.23
"""
from api.base import RestApi


class OapiEduDeptGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dept_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.dept.get'
