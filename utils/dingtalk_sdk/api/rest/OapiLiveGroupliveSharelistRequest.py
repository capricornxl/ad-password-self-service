"""
Created by auto_sdk on 2020.10.26
"""
from api.base import RestApi


class OapiLiveGroupliveSharelistRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cid = None
        self.live_uuid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.live.grouplive.sharelist'
