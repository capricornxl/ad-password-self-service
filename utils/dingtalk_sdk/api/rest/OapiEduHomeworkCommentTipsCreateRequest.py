"""
Created by auto_sdk on 2020.11.03
"""
from api.base import RestApi


class OapiEduHomeworkCommentTipsCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.attributes = None
        self.audio = None
        self.biz_code = None
        self.content = None
        self.media = None
        self.photo = None
        self.sort_order = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.homework.comment.tips.create'
