"""
Created by auto_sdk on 2020.09.23
"""
from api.base import RestApi


class OapiEduCardUserPostUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.update_post_param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.card.user.post.update'
