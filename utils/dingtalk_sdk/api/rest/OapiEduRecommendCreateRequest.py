"""
Created by auto_sdk on 2021.04.21
"""
from api.base import RestApi


class OapiEduRecommendCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.class_id = None
        self.labelList = None
        self.out_content_id = None
        self.period_code = None
        self.return_url = None
        self.subject_code = None
        self.summary = None
        self.textbook_code = None
        self.thumbnail = None
        self.title = None
        self.totalTime = None
        self.type = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.recommend.create'
