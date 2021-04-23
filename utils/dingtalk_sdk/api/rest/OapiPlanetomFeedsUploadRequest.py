"""
Created by auto_sdk on 2020.03.26
"""
from api.base import RestApi


class OapiPlanetomFeedsUploadRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.feed_app_id = None
        self.feed_info_models = None
        self.user_phone = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.planetom.feeds.upload'
