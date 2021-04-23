"""
Created by auto_sdk on 2020.11.02
"""
from api.base import RestApi


class OapiEduCircleTopiclistRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_type = None
        self.class_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.circle.topiclist'
