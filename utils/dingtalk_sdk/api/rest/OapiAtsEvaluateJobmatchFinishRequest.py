"""
Created by auto_sdk on 2020.08.10
"""
from api.base import RestApi


class OapiAtsEvaluateJobmatchFinishRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.conclusion = None
        self.ext_data = None
        self.outer_evaluate_id = None
        self.report_download_url = None
        self.result = None
        self.score = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.evaluate.jobmatch.finish'
