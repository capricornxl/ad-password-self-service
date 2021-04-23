"""
Created by auto_sdk on 2020.10.26
"""
from api.base import RestApi


class OapiAtsResumeCheckexistenceRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.resume_detail_info = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.resume.checkexistence'
