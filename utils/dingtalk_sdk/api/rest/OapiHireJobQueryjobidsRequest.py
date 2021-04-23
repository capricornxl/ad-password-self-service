"""
Created by auto_sdk on 2021.03.02
"""
from api.base import RestApi


class OapiHireJobQueryjobidsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.query_param = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.hire.job.queryjobids'
