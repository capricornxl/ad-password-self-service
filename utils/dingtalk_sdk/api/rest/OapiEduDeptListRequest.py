"""
Created by auto_sdk on 2020.06.23
"""
from api.base import RestApi


class OapiEduDeptListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.page_no = None
        self.page_size = None
        self.super_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.dept.list'
