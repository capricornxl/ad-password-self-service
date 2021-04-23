"""
Created by auto_sdk on 2020.07.13
"""
from api.base import RestApi


class OapiKacDatavVideoliveDetailListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.kac.datav.videolive.detail.list'
