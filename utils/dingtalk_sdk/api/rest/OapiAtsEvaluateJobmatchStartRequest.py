"""
Created by auto_sdk on 2020.08.09
"""
from api.base import RestApi


class OapiAtsEvaluateJobmatchStartRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.candidate_id = None
        self.category = None
        self.ext_data = None
        self.invite_url = None
        self.job_id = None
        self.outer_evaluate_id = None
        self.result_url = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.evaluate.jobmatch.start'
