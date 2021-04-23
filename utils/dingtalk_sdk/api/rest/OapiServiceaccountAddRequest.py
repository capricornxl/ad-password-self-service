"""
Created by auto_sdk on 2019.07.04
"""
from api.base import RestApi


class OapiServiceaccountAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.avatar_media_id = None
        self.brief = None
        self.desc = None
        self.name = None
        self.preview_media_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.serviceaccount.add'
