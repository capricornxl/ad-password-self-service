"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiEduClassListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.grade_id = None
        self.page_no = None
        self.page_size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.class.list'
