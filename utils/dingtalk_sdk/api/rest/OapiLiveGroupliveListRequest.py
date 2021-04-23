"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiLiveGroupliveListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cid = None
        self.from_time = None
        self.open_id = None
        self.to_time = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.live.grouplive.list'
