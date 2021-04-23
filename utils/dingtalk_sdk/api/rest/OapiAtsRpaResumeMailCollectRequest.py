"""
Created by auto_sdk on 2020.12.17
"""
from api.base import RestApi


class OapiAtsRpaResumeMailCollectRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.rpa.resume.mail.collect'
