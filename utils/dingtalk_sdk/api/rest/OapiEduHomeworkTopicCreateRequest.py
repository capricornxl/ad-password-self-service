"""
Created by auto_sdk on 2020.04.29
"""
from api.base import RestApi


class OapiEduHomeworkTopicCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.topic_items = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.homework.topic.create'
