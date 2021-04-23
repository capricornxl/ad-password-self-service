"""
Created by auto_sdk on 2020.07.23
"""
from api.base import RestApi


class OapiLiveGroupliveListbytimeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.req = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.live.grouplive.listbytime'
