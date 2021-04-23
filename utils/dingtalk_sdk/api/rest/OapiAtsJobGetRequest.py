"""
Created by auto_sdk on 2020.08.25
"""
from api.base import RestApi


class OapiAtsJobGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.job_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.job.get'
