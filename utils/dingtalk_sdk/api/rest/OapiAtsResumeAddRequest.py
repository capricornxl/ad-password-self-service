"""
Created by auto_sdk on 2021.04.01
"""
from api.base import RestApi


class OapiAtsResumeAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.resume.add'
