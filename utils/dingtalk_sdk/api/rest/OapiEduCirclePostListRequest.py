"""
Created by auto_sdk on 2020.12.24
"""
from api.base import RestApi


class OapiEduCirclePostListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open_feed_query_param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.circle.post.list'
