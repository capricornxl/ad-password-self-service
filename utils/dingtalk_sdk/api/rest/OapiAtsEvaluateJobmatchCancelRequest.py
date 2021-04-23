"""
Created by auto_sdk on 2020.07.31
"""
from api.base import RestApi


class OapiAtsEvaluateJobmatchCancelRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.ext_data = None
        self.outer_evaluate_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.evaluate.jobmatch.cancel'
