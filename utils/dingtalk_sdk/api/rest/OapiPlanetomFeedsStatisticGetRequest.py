"""
Created by auto_sdk on 2021.03.26
"""
from api.base import RestApi


class OapiPlanetomFeedsStatisticGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.anchor_id = None
        self.feed_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.planetom.feeds.statistic.get'
