"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpDingCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.attachment = None
        self.creator_userid = None
        self.receiver_userids = None
        self.remind_time = None
        self.remind_type = None
        self.text_content = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.ding.create'
